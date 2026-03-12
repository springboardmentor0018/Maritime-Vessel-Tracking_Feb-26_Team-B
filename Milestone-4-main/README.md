# 🚢 Vessel Tracker — Backend API

> **Real-time maritime vessel tracking REST API** built with Django & Django REST Framework.
> Developed as part of the **Infosys Springboard Internship** program.

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Architecture](#architecture)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Environment Variables](#environment-variables)
  - [Running the Server](#running-the-server)
  - [Docker Deployment](#docker-deployment)
- [API Reference](#api-reference)
  - [Authentication](#authentication-endpoints)
  - [Vessels](#vessel-endpoints)
  - [Voyage Replay](#voyage-replay-endpoints)
  - [Subscriptions](#subscription-endpoints)
  - [Dashboard Analytics](#dashboard-endpoints)
  - [Admin API](#admin-api-endpoints)
- [Data Source](#data-source)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [License](#license)

---

## Overview

Vessel Tracker is a robust backend REST API designed for comprehensive maritime monitoring. It empowers applications to browse, search, and subscribe to vessels globally in real-time. Built on Django and Django REST Framework, the system seamlessly integrates with the **AIS Hub API** to retrieve live Automatic Identification System (AIS) telemetry, encompassing precise geographical positions, navigation statuses, speed, course, and critical voyage details.

To ensure optimal performance and minimize external API calls, Vessel Tracker implements strategic local caching. Furthermore, it features a seamless **Demo Mode** fallback system: when run without an external API key, the system automatically populates the database with 20 highly realistic, pre-configured vessels across various types (Cargo, Tanker, Passenger, Military, etc.), making development, testing, and frontend integration completely frictionless.

---

## Features

### 🔐 Authentication & Security
- **JWT Authentication:** Secure user sessions using access and refresh tokens.
- **OTP Verification:** Email-based 6-digit OTP verification for new registrations with a 5-minute expiry window.
- **Profile Management:** Comprehensive user profiles with organizational details.

### 🚢 Core Vessel Tracking
- **Real-Time Data Injection:** Integration with AIS Hub API for live ship telemetry.
- **Smart Caching Strategy:** Local database caching to ensure minimal latency and reduced API costs.
- **Demo Mode Engine:** Automatic loading of a diverse 20-vessel simulated fleet when operating without an API key.

### 🔍 Advanced Search & Discovery
- **Paginated Listing:** Efficient and scalable retrieval of the entire tracked vessel fleet.
- **Multi-Factor Filtering:** Precision filtering by Vessel Name, Type (e.g., Cargo, Tanker), Flag State, and Cargo Type.
- **Global Search:** General keyword searching (`q=keyword`) spanning multiple vessel attributes including MMSI, IMO, and destination ports.
- **Comprehensive Profiles:** Detailed individual vessel views including dimensions (length/width/draught), real-time coordinates, course, and ETA.

### 🔔 User Subscriptions
- **Personalized Tracking:** Users can subscribe to specific vessels of interest (via MMSI).
- **Custom Notes:** Ability to attach personal/organizational notes to individual subscriptions.
- **Subscription Management:** Full CRUD operations for managing a user's fleet list.

### 🔄 Voyage Replay *(New in Milestone 4)*
- **Historical Position Tracking:** Automatic recording of vessel position snapshots on every data refresh.
- **Time-Range Playback:** Query historical positions within a specific start/end time window.
- **Latest Positions:** Quickly retrieve the N most recent positions for a vessel for live replay preview.
- **Chronological Ordering:** Positions returned in chronological order for smooth playback animation.

### 📊 Dashboard Analytics *(New in Milestone 4)*
- **Company Stats:** Fleet size, active/moored/anchored vessel counts, average speed, type breakdown, total subscribers.
- **Port Metrics:** Top destinations by vessel traffic, average speed per port, vessel types per destination.
- **Insurer Risk Data:** Per-vessel risk scoring (0–100) based on speed violations, hazardous cargo, dangerous navigation states, vessel size, and missing destination data. Aggregated risk breakdown by vessel type.

### 🛡️ Admin API *(New in Milestone 4)*
- **Health Check:** System status with DB connectivity, vessel count, last update time, demo mode status, and debug flag.
- **Application Logs:** Retrieve recent log entries from an in-memory ring buffer, filterable by severity level.
- **CSV Export:** Download complete vessel data or subscription data as CSV files for reporting and analysis.

### ⚙️ Deployment *(New in Milestone 4)*
- **Docker Support:** Production-ready Dockerfile with Python 3.11, Gunicorn, non-root user, and health checks.
- **Docker Compose:** Service orchestration with persistent volumes for database, logs, and static files.
- **Structured Logging:** Rotating file handler + console output with per-app log level configuration.
- **Production Environment:** Template with `DEBUG=False`, SMTP configuration, and Gunicorn worker settings.

### ⚙️ Administration & Integration
- **Django Admin Dashboard:** Full-featured interface for database administration encompassing Users, OTPs, Vessels, Positions, and Subscriptions.
- **CORS Configuration:** Pre-configured Cross-Origin Resource Sharing to support decoupled frontend architectures (e.g., React/Next.js/Vue).

---

## Tech Stack

| Technology | Purpose |
|---|---|
| **Python 3.10+** | Programming language |
| **Django 4.2** | Web framework |
| **Django REST Framework 3.14** | REST API toolkit |
| **Simple JWT 5.3** | JWT authentication (access & refresh tokens) |
| **django-cors-headers 4.3** | Cross-Origin Resource Sharing |
| **python-decouple 3.8** | Environment variable management |
| **requests 2.31** | HTTP client for AIS Hub API |
| **Gunicorn 21.2+** | Production WSGI server |
| **Docker** | Containerized deployment |
| **SQLite** | Default database (easily swappable) |

---

## Architecture

```
┌────────────────────────────────────────────────────────────────┐
│                        Frontend (React)                        │
│                     http://localhost:3000                       │
└─────────────────────────────┬──────────────────────────────────┘
                              │  REST API (JSON)
                              ▼
┌────────────────────────────────────────────────────────────────┐
│                   Django REST Backend                          │
│                   http://localhost:8000                         │
│                                                                │
│  ┌──────────────────┐        ┌──────────────────────────────┐  │
│  │   accounts app   │        │        vessels app           │  │
│  │                  │        │                              │  │
│  │  • Registration  │        │  • Vessel list / search      │  │
│  │  • OTP verify    │        │  • Vessel detail             │  │
│  │  • JWT login     │        │  • Data refresh              │  │
│  │  • User profile  │        │  • Subscription CRUD         │  │
│  │  • Token refresh │        │  • Voyage replay / history   │  │
│  │                  │        │  • Dashboard analytics       │  │
│  │                  │        │  • Admin API (health/export)  │  │
│  │                  │        │  • AIS Hub API service       │  │
│  └──────────────────┘        └──────────────┬───────────────┘  │
│                                             │                  │
│  ┌──────────────────────────────────────────▼───────────────┐  │
│  │                      SQLite DB                           │  │
│  │  CustomUser │ OTPCode │ Vessel │ VesselPosition │ Sub.   │  │
│  └──────────────────────────────────────────────────────────┘  │
└────────────────────────────────────┬───────────────────────────┘
                                     │  HTTP (when API key set)
                                     ▼
                         ┌───────────────────────┐
                         │   AIS Hub API          │
                         │  data.aishub.net       │
                         └───────────────────────┘
```

---

## Getting Started

### Prerequisites

- **Python 3.10** or higher
- **pip** (Python package manager)
- **Git**
- **Docker** (optional, for containerized deployment)

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/cs24182-lang/Milestone-4.git
cd Milestone-4

# 2. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate        # Linux / macOS
# venv\Scripts\activate         # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set up environment variables
cp .env.example .env
# Edit .env with your configuration (see below)

# 5. Run database migrations
python manage.py migrate

# 6. Create a superuser (optional, for admin access)
python manage.py createsuperuser

# 7. Start the development server
python manage.py runserver
```

The API will be available at **http://localhost:8000**.

### Environment Variables

Create a `.env` file in the project root (or copy from `.env.example`):

| Variable | Description | Default |
|---|---|---|
| `SECRET_KEY` | Django secret key | Auto-generated insecure key |
| `DEBUG` | Enable debug mode | `True` |
| `ALLOWED_HOSTS` | Comma-separated allowed hosts | `localhost,127.0.0.1` |
| `AIS_API_KEY` | AIS Hub API key (leave empty for demo mode) | _(empty)_ |
| `EMAIL_HOST` | SMTP server host | `smtp.gmail.com` |
| `EMAIL_PORT` | SMTP server port | `587` |
| `EMAIL_HOST_USER` | SMTP username (leave empty for console output) | _(empty)_ |
| `EMAIL_HOST_PASSWORD` | SMTP password | _(empty)_ |
| `EMAIL_USE_TLS` | Enable TLS for email | `True` |
| `DEFAULT_FROM_EMAIL` | Default sender email address | `noreply@vesseltracker.com` |
| `FRONTEND_URL` | Frontend URL for CORS | `http://localhost:3000` |
| `DATABASE_URL` | Database URL (leave empty for SQLite) | _(empty)_ |

> **💡 Tip:** For local development, you can leave `AIS_API_KEY` and `EMAIL_HOST_USER` empty. The app will use **demo vessel data** and print **OTP emails to the console** respectively.

### Running the Server

```bash
# Development
python manage.py runserver

# With a custom port
python manage.py runserver 0.0.0.0:8080
```

### Docker Deployment

```bash
# Build and run with Docker Compose
docker-compose up --build -d

# View logs
docker-compose logs -f web

# Stop
docker-compose down
```

For production deployment, copy `.env.production.example` to `.env` and configure all values.

---

## API Reference

**Base URL:** `http://localhost:8000/api/`

All responses follow a consistent JSON format:
```json
{
  "success": true,
  "message": "Description of the result",
  "data": { ... }
}
```

### Authentication Endpoints

All auth endpoints are prefixed with `/api/auth/`.

#### `POST /api/auth/register/`
Register a new user account. Sends an OTP to the provided email for verification.

**Request Body:**
```json
{
  "username": "jaswanth",
  "email": "jaswanth@example.com",
  "password": "securepassword123",
  "confirm_password": "securepassword123",
  "first_name": "Jaswanth",
  "last_name": "K",
  "phone": "+91-9876543210",
  "organization": "Infosys"
}
```
_Fields `phone`, `organization`, `first_name`, and `last_name` are optional._

**Response:** `201 Created`
```json
{
  "success": true,
  "message": "Registration successful. OTP sent to your email.",
  "data": {
    "username": "jaswanth",
    "email": "jaswanth@example.com"
  }
}
```

---

#### `POST /api/auth/verify-otp/`
Verify email address using the 6-digit OTP code. Returns JWT tokens on success.

**Request Body:**
```json
{
  "email": "jaswanth@example.com",
  "otp": "483921"
}
```

**Response:** `200 OK`
```json
{
  "success": true,
  "message": "Email verified successfully.",
  "data": {
    "access": "<jwt-access-token>",
    "refresh": "<jwt-refresh-token>",
    "user": { ... }
  }
}
```

---

#### `POST /api/auth/login/`
Login with email and password. Requires email to be verified.

**Request Body:**
```json
{
  "email": "jaswanth@example.com",
  "password": "securepassword123"
}
```

**Response:** `200 OK`
```json
{
  "success": true,
  "message": "Login successful.",
  "data": {
    "access": "<jwt-access-token>",
    "refresh": "<jwt-refresh-token>",
    "user": {
      "id": 1,
      "username": "jaswanth",
      "email": "jaswanth@example.com",
      "first_name": "Jaswanth",
      "last_name": "K",
      "phone": "+91-9876543210",
      "organization": "Infosys",
      "is_email_verified": true,
      "created_at": "2026-02-20T12:00:00Z",
      "updated_at": "2026-02-20T12:05:00Z"
    }
  }
}
```

---

#### `POST /api/auth/resend-otp/`
Resend OTP to the registered email. Invalidates any previously unused OTPs.

**Request Body:**
```json
{
  "email": "jaswanth@example.com"
}
```

---

#### `GET /api/auth/profile/`
Get the authenticated user's profile. **Requires authentication.**

**Headers:**
```
Authorization: Bearer <access_token>
```

---

#### `POST /api/auth/token/refresh/`
Refresh an expired access token using a valid refresh token.

**Request Body:**
```json
{
  "refresh": "<jwt-refresh-token>"
}
```

---

### Vessel Endpoints

All vessel endpoints require authentication via `Authorization: Bearer <access_token>` header.

#### `GET /api/vessels/`
List all tracked vessels with pagination.

**Query Parameters:**
| Param | Description | Default |
|---|---|---|
| `page` | Page number | `1` |
| `page_size` | Results per page (max 100) | `20` |

**Response:** `200 OK`
```json
{
  "count": 20,
  "next": "http://localhost:8000/api/vessels/?page=2",
  "previous": null,
  "results": [
    {
      "mmsi": "211331640",
      "imo": "9183163",
      "name": "EVER GIVEN",
      "vessel_type": "Cargo",
      "flag": "Panama",
      "cargo": "Container",
      "latitude": 31.3856,
      "longitude": 32.3617,
      "speed": 12.4,
      "nav_status": "Under way using engine",
      "last_updated": "2026-02-20T12:00:00Z"
    }
  ]
}
```

---

#### `GET /api/vessels/search/`
Search and filter vessels. All filters can be combined (AND logic).

**Query Parameters:**
| Param | Description | Example |
|---|---|---|
| `name` | Filter by vessel name (partial match) | `ever` |
| `type` | Filter by vessel type | `Cargo` |
| `flag` | Filter by flag/country | `Panama` |
| `cargo` | Filter by cargo type | `Container` |
| `q` | General search across name, MMSI, IMO, flag, cargo, destination, callsign | `singapore` |

**Example:**
```
GET /api/vessels/search/?type=Tanker&flag=Singapore
GET /api/vessels/search/?q=rotterdam
```

---

#### `GET /api/vessels/<mmsi>/`
Get full details of a specific vessel by its MMSI number.

**Response:** `200 OK`
```json
{
  "success": true,
  "data": {
    "mmsi": "211331640",
    "imo": "9183163",
    "name": "EVER GIVEN",
    "callsign": "H3RC",
    "vessel_type": "Cargo",
    "flag": "Panama",
    "cargo": "Container",
    "latitude": 31.3856,
    "longitude": 32.3617,
    "speed": 12.4,
    "course": 185.0,
    "heading": 183,
    "nav_status": "Under way using engine",
    "destination": "ROTTERDAM",
    "eta": "2026-02-25 14:00",
    "draught": 16.0,
    "length": 400.0,
    "width": 59.0,
    "subscriber_count": 5,
    "is_subscribed": false,
    "last_updated": "2026-02-20T12:00:00Z",
    "created_at": "2026-02-20T10:00:00Z"
  }
}
```

---

#### `POST /api/vessels/refresh/`
Force a refresh of vessel data from the AIS Hub API (or reload demo data).

**Response:** `200 OK`
```json
{
  "success": true,
  "message": "Vessel data refreshed. 20 vessels in database.",
  "demo_mode": true
}
```

---

### Voyage Replay Endpoints

All voyage replay endpoints require authentication. Positions are automatically recorded each time vessel data is refreshed.

#### `GET /api/vessels/<mmsi>/replay/`
Fetch historical positions for a vessel with optional time-range filtering.

**Query Parameters:**
| Param | Description | Default |
|---|---|---|
| `start` | ISO datetime — filter positions after this time | _(none)_ |
| `end` | ISO datetime — filter positions before this time | _(none)_ |
| `limit` | Max positions to return (max 1000) | `200` |

**Example:**
```
GET /api/vessels/211331640/replay/?start=2026-02-20T00:00:00Z&end=2026-02-21T00:00:00Z&limit=100
```

**Response:** `200 OK`
```json
{
  "success": true,
  "vessel": {
    "mmsi": "211331640",
    "name": "EVER GIVEN",
    "vessel_type": "Cargo"
  },
  "count": 5,
  "data": [
    {
      "id": 1,
      "vessel_mmsi": "211331640",
      "vessel_name": "EVER GIVEN",
      "latitude": 31.3856,
      "longitude": 32.3617,
      "speed": 12.4,
      "course": 185.0,
      "heading": 183,
      "nav_status": "Under way using engine",
      "recorded_at": "2026-02-20T12:00:00Z"
    }
  ]
}
```

---

#### `GET /api/vessels/<mmsi>/replay/latest/`
Fetch the N most recent positions for quick replay preview.

**Query Parameters:**
| Param | Description | Default |
|---|---|---|
| `count` | Number of recent positions (max 200) | `50` |

---

### Subscription Endpoints

All subscription endpoints require authentication.

#### `GET /api/subscriptions/`
List all of the authenticated user's vessel subscriptions.

**Response:** `200 OK`
```json
{
  "success": true,
  "count": 2,
  "data": [
    {
      "id": 1,
      "user_email": "jaswanth@example.com",
      "vessel": {
        "mmsi": "211331640",
        "name": "EVER GIVEN",
        "vessel_type": "Cargo",
        "flag": "Panama"
      },
      "notes": "Tracking Suez Canal route",
      "created_at": "2026-02-20T12:00:00Z"
    }
  ]
}
```

---

#### `POST /api/subscriptions/`
Subscribe to a vessel by its MMSI number.

**Request Body:**
```json
{
  "vessel_mmsi": "211331640",
  "notes": "Tracking Suez Canal route"
}
```
_The `notes` field is optional._

---

#### `GET /api/subscriptions/<id>/`
View details of a specific subscription.

---

#### `DELETE /api/subscriptions/<id>/`
Unsubscribe from a vessel.

**Response:** `200 OK`
```json
{
  "success": true,
  "message": "Unsubscribed from EVER GIVEN."
}
```

---

### Dashboard Endpoints

All dashboard endpoints require authentication.

#### `GET /api/dashboard/company-stats/`
Company fleet statistics overview.

**Response:** `200 OK`
```json
{
  "success": true,
  "data": {
    "total_vessels": 20,
    "active_vessels": 12,
    "moored_vessels": 6,
    "anchored_vessels": 1,
    "average_speed": 11.75,
    "total_subscribers": 3,
    "vessel_type_breakdown": [
      { "vessel_type": "Cargo", "count": 8 },
      { "vessel_type": "Tanker", "count": 4 },
      { "vessel_type": "Passenger", "count": 2 }
    ]
  }
}
```

---

#### `GET /api/dashboard/port-metrics/`
Port/destination analytics with top destinations.

**Response:** `200 OK`
```json
{
  "success": true,
  "data": {
    "total_destinations": 18,
    "top_ports": [
      {
        "destination": "ROTTERDAM",
        "vessel_count": 2,
        "avg_speed": 12.4,
        "vessel_types": ["Cargo"]
      },
      {
        "destination": "SINGAPORE",
        "vessel_count": 1,
        "avg_speed": 0.0,
        "vessel_types": ["Cargo"]
      }
    ]
  }
}
```

---

#### `GET /api/dashboard/risk-data/`
Insurer risk assessment with per-vessel risk scoring.

**Risk Scoring Model (0–100):**

| Factor | Points | Condition |
|---|---|---|
| High speed | +30 | Speed > 15 kn |
| Moderate speed | +10 | Speed > 10 kn |
| Dangerous nav status | +25 | Not under command, aground, etc. |
| Large vessel | +15 | Length > 300m |
| Hazardous cargo | +20 | Tanker with Crude Oil/LNG/Petroleum/Chemicals |
| No destination | +10 | Destination field empty |

**Response:** `200 OK`
```json
{
  "success": true,
  "data": {
    "total_assessed": 20,
    "high_risk_count": 3,
    "medium_risk_count": 8,
    "low_risk_count": 9,
    "average_risk_score": 28.5,
    "risk_by_type": {
      "Cargo": 22.5,
      "Tanker": 45.0,
      "Passenger": 15.0
    },
    "high_risk_vessels": [
      {
        "mmsi": "477118800",
        "name": "ORIENTAL DRAGON",
        "vessel_type": "Tanker",
        "risk_score": 60.0,
        "risk_factors": [
          "Moderate speed: 13.5 kn",
          "Large vessel: 336.0m length",
          "Hazardous cargo: Petroleum Products"
        ],
        "speed": 13.5,
        "nav_status": "Under way using engine"
      }
    ]
  }
}
```

---

### Admin API Endpoints

All admin endpoints require **staff/admin** authentication (`is_staff=True`).

#### `GET /api/admin-api/health/`
System health check with database status, counts, and configuration info.

**Response:** `200 OK`
```json
{
  "success": true,
  "data": {
    "status": "operational",
    "timestamp": "2026-03-11T08:00:00Z",
    "database": "healthy",
    "demo_mode": true,
    "debug_mode": true,
    "counts": {
      "vessels": 20,
      "users": 5,
      "subscriptions": 3,
      "position_snapshots": 100
    },
    "last_vessel_update": "2026-03-11T07:55:00Z"
  }
}
```

---

#### `GET /api/admin-api/logs/`
Retrieve recent application log entries.

**Query Parameters:**
| Param | Description | Default |
|---|---|---|
| `count` | Number of log entries (max 500) | `100` |
| `level` | Minimum log level filter | _(all)_ |

**Example:**
```
GET /api/admin-api/logs/?count=50&level=ERROR
```

---

#### `GET /api/admin-api/export/vessels/`
Download all vessel data as a CSV file.

**Response:** CSV file download (`vessels_export_20260311_080000.csv`)

---

#### `GET /api/admin-api/export/subscriptions/`
Download all subscription data as a CSV file.

**Response:** CSV file download (`subscriptions_export_20260311_080000.csv`)

---

## Data Source

### AIS Hub API

This project integrates with the [AIS Hub](https://www.aishub.net/) API for real-time vessel tracking data. AIS Hub aggregates Automatic Identification System (AIS) data from a global network of receivers.

- **API Endpoint:** `http://data.aishub.net/ws.php`
- **Data Format:** JSON
- **Authentication:** API key (passed via the `AIS_API_KEY` environment variable)

### Demo Mode

When no `AIS_API_KEY` is configured, the application runs in **demo mode** with 20 pre-loaded vessels covering diverse types and global locations:

| Type | Count | Example Vessels |
|---|---|---|
| Cargo | 8 | EVER GIVEN, MAERSK EDINBURGH, CMA CGM JACQUES SAADE |
| Tanker | 4 | PACIFIC VOYAGER, OCEAN GRACE, ORIENTAL DRAGON |
| Passenger | 2 | HARMONY OF THE SEAS, TAHITI NUI |
| Fishing | 2 | ATLANTIC PIONEER, WINDWARD HUNTER |
| Tug | 1 | DUTCH SPIRIT |
| Military | 1 | HMS QUEEN ELIZABETH |
| Sailing | 1 | SOUTHERN CROSS |

---

## Project Structure

```
Milestone-4/
├── manage.py                       # Django management script
├── requirements.txt                # Python dependencies
├── Dockerfile                      # Production Docker image
├── docker-compose.yml              # Docker orchestration
├── .env.example                    # Dev environment template
├── .env.production.example         # Production environment template
├── .gitignore                      # Git ignore rules
├── db.sqlite3                      # SQLite database (auto-generated)
│
├── vessel_tracker/                 # Django project configuration
│   ├── settings.py                 # Settings (JWT, CORS, DB, Email, Logging)
│   ├── urls.py                     # Root URL routing (v2.0)
│   ├── wsgi.py                     # WSGI entry point
│   └── asgi.py                     # ASGI entry point
│
├── accounts/                       # User authentication app
│   ├── models.py                   # CustomUser, OTPCode models
│   ├── serializers.py              # Register, Login, OTP, Profile serializers
│   ├── views.py                    # Auth API views (register, login, OTP, profile)
│   ├── urls.py                     # Auth URL routing
│   ├── utils.py                    # OTP generation & email sending
│   └── admin.py                    # Admin configuration
│
└── vessels/                        # Vessel tracking app
    ├── models.py                   # Vessel, VesselPosition, Subscription models
    ├── serializers.py              # Vessel, Replay, Dashboard, Risk serializers
    ├── views.py                    # Vessel, Replay, Dashboard views
    ├── admin_views.py              # Admin API views (health, logs, export)
    ├── urls.py                     # All vessel/replay/dashboard/admin URL routing
    ├── services.py                 # AIS Hub API client + demo data + position recording
    └── admin.py                    # Admin configuration (Vessel, Position, Subscription)
```

---

## JWT Token Usage

All protected endpoints require a valid JWT access token in the `Authorization` header:

```
Authorization: Bearer <access_token>
```

| Token | Lifetime | Notes |
|---|---|---|
| **Access Token** | 1 hour | Used for API authentication |
| **Refresh Token** | 7 days | Used to obtain a new access token |

Refresh tokens are **rotated** — each refresh generates a new refresh token and invalidates the old one.

---

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## License

This project is developed as part of the **Infosys Springboard Internship** program.

---

<p align="center">
  Built with ❤️ using Django & Django REST Framework
</p>
