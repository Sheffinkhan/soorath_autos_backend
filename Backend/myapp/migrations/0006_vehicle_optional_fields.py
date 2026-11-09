from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0005_alter_vehicle_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vehicle',
            name='kilometers',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='vehicle',
            name='fuel',
            field=models.CharField(blank=True, choices=[('Petrol', 'Petrol'), ('Diesel', 'Diesel'), ('Electric', 'Electric')], max_length=10),
        ),
        migrations.AlterField(
            model_name='vehicle',
            name='transmission',
            field=models.CharField(blank=True, choices=[('Manual', 'Manual'), ('Automatic', 'Automatic'), ('Semi Automatic', 'Semi Automatic')], max_length=30),
        ),
        migrations.AlterField(
            model_name='vehicle',
            name='status',
            field=models.CharField(blank=True, choices=[('Available', 'Available'), ('Sold', 'Sold')], default='Available', max_length=10),
        ),
    ]
