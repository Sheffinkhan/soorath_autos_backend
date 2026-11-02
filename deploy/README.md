# Deploying the backend on Oracle Cloud Always Free

This runs Django, PostgreSQL and nginx together on one free Arm server. Static files are served by WhiteNoise, and images stay in S3 or Cloudflare R2. Redis isn't needed.

## Before you start

1. **Replace the exposed secrets.** `Backend/.env` was committed to this public repo and is still in git history. Deactivate that AWS key in IAM, and use a new `SECRET_KEY` and database password below.
2. **Leave the current EC2 server alone.** This branch removes `Backend/.env` and `Backend/venv` from git, so running `git pull` there after merging would delete them and take the site down. Shut that server down once Oracle is working.
3. **Merge this branch into `main`.** The steps below clone `main`.

## 1. Create the server

In the Oracle Cloud console, create a compute instance:

- **Region:** your home region. Instances must be created there, and it can't be changed after sign-up.
- **Image:** Ubuntu 24.04 (the aarch64 build)
- **Shape:** `VM.Standard.A1.Flex` with 2 OCPUs and 12 GB of memory. Going over this is outside the free allowance.
- **Boot volume:** 50 GB (200 GB in total is free)

If you see "out of host capacity", try another availability domain or retry later.

Then add ingress rules to the subnet's security list for TCP ports 80 and 443 from `0.0.0.0/0`.

## 2. Open the server firewall

Oracle's Ubuntu images block these ports by default, as well as the security list above. Connect over SSH as `ubuntu`, then find the line number of the `REJECT` rule:

```bash
sudo iptables -L INPUT --line-numbers
```

Use that number in place of `LINE` below, so the new rules sit above the `REJECT` rule:

```bash
sudo iptables -I INPUT LINE -m state --state NEW -p tcp --dport 80 -j ACCEPT
sudo iptables -I INPUT LINE -m state --state NEW -p tcp --dport 443 -j ACCEPT
sudo netfilter-persistent save
```

## 3. Install the packages

```bash
sudo apt update
sudo apt install -y git nginx postgresql python3-venv certbot python3-certbot-nginx
```

## 4. Create the database

Replace `NEW_DB_PASSWORD` with the new password:

```bash
sudo -u postgres psql -c "CREATE ROLE soorathuser LOGIN PASSWORD 'NEW_DB_PASSWORD';"
sudo -u postgres psql -c "CREATE DATABASE soorathautos OWNER soorathuser;"
```

To bring over your live data, run this on the EC2 server, using the database name and user from its `.env`:

```bash
pg_dump -Fc -h localhost -U DB_USER DB_NAME > soorath.dump
```

Copy `soorath.dump` to `/tmp` on the Oracle server, then restore it there:

```bash
sudo -u postgres pg_restore --no-owner --role=soorathuser -d soorathautos /tmp/soorath.dump
```

## 5. Install the app

```bash
sudo mkdir -p /opt/soorath_autos_backend
sudo chown ubuntu:ubuntu /opt/soorath_autos_backend
git clone https://github.com/MaCo-Labs/soorath_autos_backend.git /opt/soorath_autos_backend
cd /opt/soorath_autos_backend/Backend
python3 -m venv venv
venv/bin/pip install -r requirements.txt
cp .env.example .env
chmod 600 .env
```

Create a new `SECRET_KEY`:

```bash
python3 -c "import secrets; print(secrets.token_urlsafe(50))"
```

Edit `.env` with `nano .env`:

- Set `SECRET_KEY`, `DB_PASSWORD` and the image storage values.
- Set `ALLOWED_HOSTS` to your domain, and `CSRF_TRUSTED_ORIGINS` to the same domain starting with `https://`.
- Set `CORS_ALLOWED_ORIGINS` to your frontend's address.

If you don't have a domain, `SERVER_IP.nip.io` works with your server's public IP address.

Then prepare the app:

```bash
venv/bin/python manage.py migrate
venv/bin/python manage.py collectstatic --noinput
```

If you started with an empty database, create an admin user too:

```bash
venv/bin/python manage.py createsuperuser
```

## 6. Start the app and nginx

Replace `YOUR_DOMAIN` in the first command:

```bash
sudo sed 's/YOUR_DOMAIN/your-domain.example.com/' /opt/soorath_autos_backend/deploy/soorath-backend.nginx.conf | sudo tee /etc/nginx/sites-available/soorath-backend > /dev/null
sudo ln -s /etc/nginx/sites-available/soorath-backend /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default
sudo nginx -t
sudo systemctl reload nginx
sudo cp /opt/soorath_autos_backend/deploy/soorath-backend.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now soorath-backend
```

## 7. Turn on HTTPS

Your frontend uses HTTPS, so browsers will block calls to a backend that doesn't.

```bash
sudo certbot --nginx -d your-domain.example.com
```

## 8. Test it and switch over

```bash
curl https://your-domain.example.com/api/vehicles/
```

Also log in at `https://your-domain.example.com/admin/`, upload an image, and try a search with a typo. Then point the frontend's API address at the new domain.

## 9. Set up backups

Oracle can reclaim the server, so keep copies of your data somewhere else.

```bash
sudo mkdir -p /var/backups/soorath
sudo chown postgres:postgres /var/backups/soorath
sudo -u postgres crontab -e
```

Add this line to save a dump every night and keep 14 days of them:

```
0 2 * * * pg_dump -Fc soorathautos > /var/backups/soorath/soorath-$(date +\%F).dump && find /var/backups/soorath -name '*.dump' -mtime +14 -delete
```

Copy those files off the server regularly, for example to a private bucket with `rclone`. Don't put them in your image bucket, because its files are public.

## Updating the app

```bash
cd /opt/soorath_autos_backend
git pull
cd Backend
venv/bin/pip install -r requirements.txt
venv/bin/python manage.py migrate
venv/bin/python manage.py collectstatic --noinput
sudo systemctl restart soorath-backend
```

## Watch for idle reclaim

Oracle treats an instance as idle if, over 7 days, CPU (95th percentile), network and memory use are all under 20%. A quiet site could qualify, so check the instance's metrics in the console after the first week.
