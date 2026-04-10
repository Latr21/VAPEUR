# VAPEUR - Digital Game Store Frontend Microservice

This repository contains a lightweight Python Django frontend web application designed to serve as a dematerialized video game shop (similar to Steam). It is architected to run as a microservice within a Kubernetes cluster.

## 🚀 Features

- **Steam-inspired UI**: A modern, dark-themed responsive interface using **Tailwind CSS** (via CDN).
- **Game Library**: A homepage displaying a curated grid of video games with titles, prices, and high-quality thumbnails.
- **Authentication**: Complete user registration (Sign Up) and authentication (Sign In) flows.
- **Microservice Ready**:
    - **Pluggable Auth Layer**: A dedicated `AuthService` abstraction in `gamestore/services/auth_service.py`. It currently uses local Django Auth for the POC but is designed to be easily swapped for REST calls to an external `AuthManager` microservice.
    - **Database Agnostic**: Initialized with SQLite for rapid development, ready to connect to a PostgreSQL sidecar in production via environment variables.
    - **Lightweight Image**: Built on `python:3.11-slim` with `Gunicorn` as the production WSGI server.
    - **Security**: Runs as a non-root user (`vapeuruser`) within the container.

## 🛠️ Project Structure

```text
vapeur_front/
├── config/              # Project configuration (settings, urls, wsgi)
├── gamestore/           # Core application logic
│   ├── services/        # Abstraction layer for external microservices
│   ├── templates/       # Django HTML templates (Tailwind CSS)
│   ├── views.py         # Controllers for Home, Login, Signup
│   └── urls.py          # App-specific routing
├── Dockerfile           # Production-ready container definition
├── requirements.txt     # Python dependencies
└── manage.py            # Django management script
```

## 📦 How to Run

### 1. Locally (Python)

If you have Python installed:

```bash
cd vapeur_front

# Create a virtual environment (optional but recommended)
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run migrations to initialize the SQLite database
python3 manage.py migrate

# Create a superuser to access the Django Admin (/admin)
python3 manage.py createsuperuser

# Start the development server
python3 manage.py runserver
```
Access the app at `http://127.0.0.1:8000`.

### 2. Using Docker (Recommended for K8s)

To build and run the microservice as a container:

```bash
# Build the image
docker build -t vapeur-front .

# Run the container
docker run -p 8000:8000 vapeur-front
```
Access the app at `http://localhost:8000`.

## 🎮 Using the Application

### Available Routes

- **`/`**: Home page displaying the game library (using mock data).
- **`/signup/`**: Create a new account.
- **`/login/`**: Sign in to your account.
- **`/logout/`**: Log out from the current session.
- **`/admin/`**: Django administration interface (requires superuser).

### Mock Data Notice
The current version of the store displays hardcoded mock games in `gamestore/views.py`. In a future iteration, these will be fetched from a `Catalog` microservice.

### Authentication Flow
The app uses a pluggable `AuthService`. By default, it uses the local Django database. To test registration:
1. Navigate to `/signup/`.
2. Fill in your details.
3. Once redirected to `/login/`, enter your credentials.
4. You will be redirected to the Home page with a welcome message.

## 🌐 Kubernetes Integration

To integrate this frontend into your ecosystem:

1. **Authentication**: Update `gamestore/services/auth_service.py` to replace the local Django Auth calls with `requests.post()` calls to your `AuthManager` service URL.
2. **Database**: In `config/settings.py`, configure the `DATABASES` setting to point to your PostgreSQL sidecar service using environment variables (e.g., `os.environ.get('DB_HOST')`).
3. **Environment Variables**: Use a ConfigMap or Secret in Kubernetes to inject the `SECRET_KEY` and other sensitive configurations.

---
*Developed as a Proof of Concept for the VAPEUR ecosystem.*
