🚗 Soorath Autos – Full Stack Car Dealership Platform
🚀 Overview
Soorath Autos is a full-stack web application developed for a real used car dealership in Muvattupuzha, Kerala. The platform allows users to browse, search, and view vehicle listings, while providing an admin system to manage inventory through a secure API-driven architecture.
🧱 Architecture
Frontend: React + Vite
Backend: Django + Django REST Framework
Database: PostgreSQL
Storage: AWS S3
Deployment: Nginx (production)
The system follows a decoupled architecture, where the frontend communicates with backend APIs.
🔥 Key Features
👤 User Features
Browse and search vehicle listings
Advanced filtering (fuel, search, etc.)
Detailed vehicle pages with image gallery
Fast and responsive UI using React
🔐 Admin Features
Secure admin APIs with JWT authentication
Add, update, delete vehicle listings
Upload multiple images per vehicle
Manage vehicle status (available/sold, featured)
⚙️ Backend Highlights
🔎 Advanced Search System
Implemented PostgreSQL full-text search + trigram similarity
Handles typos and partial matches
Uses pg_trgm extension for fuzzy search
🔐 JWT Authentication
Token-based authentication (access + refresh tokens)
Protected admin routes
Axios interceptors for automatic token handling
📦 REST API Design
Fully RESTful architecture
Pagination support
Filtering and query parameters
Structured JSON responses
🖼 Image Handling
Images stored in AWS S3 (not local storage)
Scalable and production-ready file handling
🔄 Example Data Flow
User searches for a car (e.g., "Swift")
React sends request → /api/vehicles/?search=Swift
Django processes request with search + filters
PostgreSQL runs fuzzy + full-text search
Results returned as JSON
React updates UI dynamically
🛠 Tech Stack
Python
Django
Django REST Framework
React (Vite)
PostgreSQL
AWS S3
Nginx
👨‍💻 My Contribution
Built backend APIs using Django REST Framework
Implemented vehicle management system (CRUD)
Developed advanced search using PostgreSQL (pg_trgm)
Integrated JWT authentication and route protection
Designed database models and relationships
Configured API filtering, pagination, and serializers
Worked on frontend integration with React
📌 Key Highlights
Real-world production project
API-first architecture
Advanced database optimization (search indexing)
Scalable file storage using AWS
🔗 Live Project
https://www.soorathautos.in/

🚀 Deployment
Every merge or push to main deploys automatically (GitHub Actions, .github/workflows/deploy.yml):
it pulls the code on the EC2 server, applies migrations, restarts gunicorn and checks the API responds.
Progress and logs are in the Actions tab.
