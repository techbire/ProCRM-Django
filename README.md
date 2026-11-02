# Pro Customer Relationship Management (CRM) System

A clean, beginner-friendly CRM web application built with **Python Django**, **HTML5**, **CSS3**, **Bootstrap 5**, and **SQLite**.

---

## 📖 Table of Contents
1. [Project Overview](#project-overview)
2. [Key Features](#key-features)
3. [Technology Stack](#technology-stack)
4. [Project Folder Structure](#project-folder-structure)
5. [Step-by-Step Installation & Run Guide](#step-by-step-installation--run-guide)
6. [Pre-configured Demo Credentials](#pre-configured-demo-credentials)
7. [Explanation of Key Files & Architecture](#explanation-of-key-files--architecture)
8. [Database Models & Relationships](#database-models--relationships)
9. [Running Automated Tests](#running-automated-tests)

---

## 1. Project Overview
This application provides small businesses and sales teams with an intuitive tool to:
- Store and organize customer profiles and contact details.
- Track sales prospects through five pipeline stages: *New*, *Contacted*, *Interested*, *Converted*, and *Lost*.
- Convert high-intent leads into customer records with a single click.
- Log interaction history (phone calls, meetings, emails, and notes) linked to customers.
- Visualize sales metrics and recent operations on an executive dashboard.

---

## 2. Key Features

### 🔐 User Authentication
- User Registration with form validation (password matching and uniqueness checks).
- Secure login and logout powered by Django's built-in session authentication.
- Full route protection using `@login_required` decorators.

### 📊 Executive Dashboard
- **Total Customers** metric counter.
- **Total Leads** metric counter.
- **Active Leads** in the pipeline (*New*, *Contacted*, *Interested*).
- **Converted Leads** and conversion rate calculation.
- Recent 5 Leads and Recent 5 Customers preview tables.
- Recent interaction activity timeline with timestamps and author attribution.

### 👥 Customer Management (Full CRUD)
- **Add New Customer**: capture full name, email, phone, company, and physical address.
- **Customer List**: clean, readable table with search functionality across name, company, email, and phone.
- **Customer Profile View**: detailed contact card, linked leads table, activity timeline, and quick interaction logger.
- **Edit Customer**: update customer contact info.
- **Delete Customer**: delete with confirmation safeguard.

### 🎯 Sales Lead Pipeline (Full CRUD)
- **Track Status**: *New*, *Contacted*, *Interested*, *Converted*, *Lost*.
- **Acquisition Source Tracking**: *Website*, *Referral*, *Social Media*, *Cold Call*, *Email Campaign*, *Event*, *Other*.
- **Status Filter Chips**: filter leads instantly by clicking status pills.
- **One-Click Lead Conversion**: convert a prospective lead into a full customer profile automatically.
- **Lead Detail & Edit Pages**.

### 📝 Activity Management
- Record every customer interaction:
  - 📞 **Phone Call**
  - 🤝 **Meeting**
  - ✉️ **Email**
  - 📝 **General Note**
- Log interactions from the customer profile, lead profile, or the global activity logger.
- Chronological timeline with filter by activity type and full-text search.

---

## 3. Technology Stack
- **Backend**: Python 3.10+ / Django 5.x
- **Database**: SQLite3 (`db.sqlite3`)
- **ORM**: Django Object-Relational Mapping (ORM)
- **Frontend**: HTML5, CSS3, Bootstrap 5.3.3 (via CDN), Bootstrap Icons 1.11.3 (via CDN)
- **Authentication**: Django built-in `django.contrib.auth`

---

## 4. Project Folder Structure

```
djyango/
│
├── manage.py                          # Django command-line execution utility
├── requirements.txt                   # Project Python dependencies
├── db.sqlite3                         # SQLite database with sample data
├── README.md                          # Comprehensive documentation
│
├── crm_project/                       # Project configuration folder
│   ├── __init__.py
│   ├── asgi.py                        # ASGI configuration for async servers
│   ├── settings.py                    # Global Django settings (apps, DB, auth)
│   ├── urls.py                        # Root URL routing
│   └── wsgi.py                        # WSGI configuration for web servers
│
└── crm/                               # Core CRM Application
    ├── __init__.py
    ├── admin.py                       # Django Admin configuration for models
    ├── apps.py                        # App configuration
    ├── forms.py                       # Bootstrap-styled forms (Customer, Lead, Activity, Auth)
    ├── models.py                      # Database models (Customer, Lead, Activity)
    ├── tests.py                       # Automated test suite
    ├── urls.py                        # App URL routes
    ├── views.py                       # View logic & controllers
    │
    ├── management/                    # Custom management commands
    │   └── commands/
    │       ├── __init__.py
    │       └── seed_data.py           # Populates 25 customers, 25 leads, 30 activities
    │
    ├── migrations/                    # Database migration files
    │   ├── 0001_initial.py
    │   └── __init__.py
    │
    ├── static/crm/                    # Static assets
    │   ├── css/
    │   │   └── style.css              # Custom styling for dashboard, cards & sidebar
    │   └── js/
    │       └── main.js                # Mobile sidebar toggle & auto-dismiss alerts
    │
    └── templates/crm/                 # HTML templates
        ├── base.html                  # Master layout with sidebar & topbar
        ├── dashboard.html             # Statistics dashboard & overview
        │
        ├── auth/
        │   ├── login.html             # Login page
        │   └── register.html          # Registration page
        │
        ├── customers/
        │   ├── customer_list.html     # Customer directory table with search
        │   ├── customer_detail.html   # Customer profile, leads & activity timeline
        │   ├── customer_form.html     # Add / Edit customer form
        │   └── customer_confirm_delete.html # Deletion confirmation
        │
        ├── leads/
        │   ├── lead_list.html         # Leads pipeline with status chips & search
        │   ├── lead_detail.html       # Lead detail & conversion trigger
        │   ├── lead_form.html         # Add / Edit lead form
        │   └── lead_confirm_delete.html # Deletion confirmation
        │
        └── activities/
            ├── activity_list.html     # Activity history audit log with filters
            └── activity_form.html     # Log new interaction form
```

---

## 5. Step-by-Step Installation & Run Guide

### Step 1: Open Terminal in the Project Directory
```bash
cd djyango
```

### Step 2: (Optional but Recommended) Create a Virtual Environment
```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Required Packages
```bash
pip install -r requirements.txt
```

### Step 4: Run Migrations
Applies the database schema to SQLite:
```bash
python manage.py migrate
```

### Step 5: (Already Seeded) Populate 25 Customers, 25 Leads & 30 Activities
The database comes pre-seeded. If you ever reset or recreate `db.sqlite3`, run:
```bash
python manage.py seed_data
```

### Step 6: Start the Development Server
```bash
python manage.py runserver
```

Open your browser and navigate to:
👉 **http://127.0.0.1:8000/**

---

## 6. Pre-configured Demo Credentials

| Role | Username | Password |
|---|---|---|
| **Administrator / Staff** | `admin` | `admin123` |

You can also use the **Register** link on the login page to create any number of custom user accounts.

You can also access the **Django Admin Panel** at:
👉 **http://127.0.0.1:8000/admin/**

---

## 7. Explanation of Key Files & Architecture

### `crm/models.py`
Defines the structure of our database tables using Python classes:
- **`Customer`**: Represents a paying or registered client with full contact info and address.
- **`Lead`**: Represents a prospective client in the sales pipeline with status (`New`, `Contacted`, `Interested`, `Converted`, `Lost`), source, and an optional link to `Customer`.
- **`Activity`**: Represents an interaction event (`Call`, `Meeting`, `Email`, `Note`) linked via a Foreign Key to `Customer` and optionally `Lead`.

### `crm/views.py`
Contains the business logic:
- `dashboard_view`: Queries the database using Django ORM aggregation methods (`.count()`, `.filter()`) and passes metrics to the dashboard template.
- `customer_list`, `customer_detail`, `customer_create`, `customer_update`, `customer_delete`: Implements standard CRUD for customers with search filtering via `Q()` objects.
- `lead_list`, `lead_detail`, `lead_create`, `lead_update`, `lead_delete`: Implements CRUD and status filtering for leads.
- `lead_convert`: A helper workflow that promotes a prospective lead into an active Customer record in one click and records an activity audit note.
- `activity_list`, `activity_create`, `activity_delete`: Handles interaction logging.

### `crm/forms.py`
Generates HTML form controls and performs server-side data validation:
- `CustomerForm`, `LeadForm`, and `ActivityForm` inherit from `forms.ModelForm`, automatically mapping model fields to form inputs while adding Bootstrap classes (`form-control`, `form-select`).
- `UserRegistrationForm` validates unique emails and ensures password confirmation matches.

### `crm/urls.py`
Maps browser URL paths (e.g. `/customers/`, `/leads/add/`) to the corresponding Python view functions.

### `crm/templates/crm/base.html`
The master layout template. Includes:
- A responsive dark sidebar with navigation links and active state detection.
- A top header with user status and logout button.
- Bootstrap 5 alert messages banner for instant feedback (e.g., "Customer created successfully!").
- CDN links for Bootstrap 5 and Bootstrap Icons.

---

## 8. Database Models & Relationships

```
+--------------------+               +--------------------+
|      Customer      |               |        User        |
+--------------------+               +--------------------+
| id (PK)            |               | id (PK)            |
| name               |               | username           |
| email (Unique)     |               | password           |
| phone              |               +---------+----------+
| company            |                         |
| address            |                         | created_by (FK)
| created_at         |                         |
+---------+----------+                         |
          |                                    |
          | 1:N (One Customer has Many Leads)  |
          v                                    v
+--------------------+               +--------------------+
|        Lead        |<--------------|      Activity      |
+--------------------+  (Optional FK)|+--------------------+
| id (PK)            |               | id (PK)            |
| customer (FK, Null)|               | customer (FK)      |
| name               |               | lead (FK, Null)    |
| email              |               | activity_type      |
| phone              |               | subject            |
| source             |               | notes              |
| status             |               | date               |
| notes              |               | created_by (FK)    |
| created_at         |               | created_at         |
+--------------------+               +--------------------+
```

---

## 9. Running Automated Tests

To run the built-in test suite:
```bash
python manage.py test
```

This validates:
- Redirection to login for unauthenticated users.
- Metric calculations on the dashboard.
- Customer CRUD operations and search filtering.
- Lead CRUD and one-click lead conversion to customer.
- Activity logging and association with customers.

