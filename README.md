# StudentHub — Enterprise Student Management & Academic Administration System

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-5.1-092E20?style=flat&logo=django&logoColor=white)](https://www.djangoproject.com/)
[![Django REST Framework](https://img.shields.io/badge/DRF-3.17-red?style=flat&logo=django&logoColor=white)](https://www.django-rest-framework.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-4169E1?style=flat&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Bootstrap 5](https://img.shields.io/badge/Bootstrap-5.3-7952B3?style=flat&logo=bootstrap&logoColor=white)](https://getbootstrap.com/)
[![OpenAPI 3.0](https://img.shields.io/badge/OpenAPI-3.0-6BA539?style=flat&logo=openapi-initiative&logoColor=white)](https://swagger.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**StudentHub** is a comprehensive, production-ready **Student Management & Academic Administration System** engineered for universities, colleges, and educational institutes. Built with **Python 3.11, Django 5, Django REST Framework (DRF), SimpleJWT, PostgreSQL**, and **Bootstrap 5**, the platform offers a dual architecture: an interactive Server-Side Rendered (SSR) Web Portal alongside a fully documented RESTful API backend.

---

## 🔑 Demo Logins & Access Credentials

You can test the live features across all **4 system roles** immediately using the pre-seeded demo accounts below (or run `python manage.py seed_data` after local setup):

| Role | Username | Password | Full Name | Access & Portal Scope |
|---|---|---|---|---|
| **Super Admin** | `admin` | `Admin@123` | Super Admin | Full System Control, Department & Faculty Config, Global Analytics, Audit Logs |
| **Admin / Staff** | `staff1` | `Staff@123` | Karan Mehta | Student Directory & Enrollment, Fee Structure Setup, Announcement Publishing |
| **Teacher / Faculty** | `prof.sharma` | `Teacher@123` | Rajesh Sharma | Subject Workload, Session Attendance Entry, Exam Grade Scoring, Assignment Grading |
| **Teacher / Faculty** | `prof.patel` | `Teacher@123` | Ananya Patel | Subject Workload, Session Attendance Entry, Exam Grade Scoring, Assignment Grading |
| **Student (CSE)** | `d.jahidbasha` | `Student@123` | D. Jahid Basha | Personal Dashboard, Attendance Tracker, Transcript & Marks, Fee Receipts |
| **Student (ECE)** | `k.hussain` | `Student@123` | K. Hussain | Personal Dashboard, Attendance Tracker, Transcript & Marks, Fee Receipts |
| **Student (CSE)** | `b.indra` | `Student@123` | B. Indra | Personal Dashboard, Attendance Tracker, Transcript & Marks, Fee Receipts |
| **Student (ECE)** | `narasimha` | `Student@123` | Narasimha Rao | Personal Dashboard, Attendance Tracker, Transcript & Marks, Fee Receipts |
| **Student (CSE)** | `kiran` | `Student@123` | Kiran Kumar | Personal Dashboard, Attendance Tracker, Transcript & Marks, Fee Receipts |
| **Student (CSE)** | `rahul.kumar` | `Student@123` | Rahul Kumar | Personal Dashboard, Attendance Tracker, Transcript & Marks, Fee Receipts |

> 💡 **Note**: All 15 enrolled student demo accounts use the standard password `Student@123`.

---

## 🌟 Key System Features

### 🔐 1. Authentication & Role-Based Access Control (RBAC)
- **Custom User Model**: Built on Django’s AbstractUser with 4 explicit roles: `SUPERADMIN`, `ADMIN`, `TEACHER`, and `STUDENT`.
- **Dual Authentication Engine**: Stateless **JWT Access/Refresh Tokens** for REST APIs + Session Auth for Web UI.
- **Granular Permissions**: Object-level security ensuring students only view their own records, teachers manage only assigned subjects, and admins maintain system-wide governance.

### 🏛️ 2. Core Academic Administration
- Hierarchy management: **Departments** (e.g., CSE, ECE), **Courses**, **Subjects**, **Academic Years**, and **Class Sections**.
- Automated subject code generation and teacher allocations per class section.

### 👨‍🎓 3. Student Lifecycle & Profile Management
- Interactive **"Add New Student"** workflow with automatic unique ID generation (e.g., `STU-2026-001`).
- Student profile customization, document attachments, emergency contacts, academic enrollment history, and status updates (`ACTIVE`, `SUSPENDED`, `GRADUATED`).

### 📅 4. Attendance Engine & Automated Low-Attendance Warnings
- Session-based attendance logging per class section by assigned teachers.
- Real-time calculation formula:
  $$\text{Attendance } \% = \left(\frac{\text{Sessions Attended}}{\text{Total Sessions}}\right) \times 100$$
- Visual **Low Attendance Warning Badges (< 75%)** flagged on both student and teacher dashboards.

### 📝 5. Examinations & Automated Grade Evaluation
- Scheduling for Mid-Term, Final, Quiz, and Practical examinations.
- Automated letter grade computation (`A+`, `A`, `B+`, `B`, `C`, `D`, `F`) based on institution scoring thresholds.
- Dynamic report cards and downloadable student academic transcripts.

### 📚 6. Assignments & Online Submissions
- Teachers publish digital coursework with file attachments and target deadlines.
- Students submit solution files; automated system flagging for `SUBMITTED`, `LATE`, or `PENDING` states.

### 💳 7. Fee Management & Payment Tracking (Indian Rupees - ₹)
- Dynamic semester fee structure setup in **Indian Rupees (₹ / INR)**.
- Automated computation of total fees, discounts, payments made, and outstanding balance.
- Payment transaction recording with digital payment receipt data.

### 📢 8. Targeted Notice Board & Campus Announcements
- Priority announcements (`LOW`, `MEDIUM`, `HIGH`, `URGENT`) targeted by audience scope: All Users, Specific Department, or Specific Class.

### 📊 9. Role-Tailored Analytical Dashboards
- **Admin View**: Institution total stats, department distribution, fee collection summary, recent audit actions.
- **Teacher View**: Daily teaching schedule, pending attendance markers, ungraded assignments.
- **Student View**: Attendance gauge meter, GPA transcript summary, upcoming exam schedules, fee dues.

---

## 🛠️ Technology Stack

| Layer | Technologies & Libraries |
|---|---|
| **Backend Framework** | Python 3.11+, Django 5.1, Django REST Framework (DRF 3.17) |
| **Authentication & Security** | SimpleJWT (JWT Tokens), Django RBAC, CORS Headers, Passlib |
| **Frontend UI** | Bootstrap 5.3, HTML5, CSS3, JavaScript (ES6+), FontAwesome Icons |
| **Database** | PostgreSQL 15 (Production) / SQLite3 (Local Development) |
| **API Documentation** | OpenAPI 3.0, Swagger UI, ReDoc via `drf-spectacular` |
| **DevOps & Testing** | Django Test Framework, Coverage.py, Git, Postman |

---

## 🏗️ Architecture & Modular Project Structure

StudentHub uses a clean, modular Django app structure where each domain is decoupled into its own app inside the `apps/` directory:

```text
Student Management System/
│
├── apps/                         # Modular Application Domain Directory
│   ├── accounts/                 # Custom User Model, JWT Auth, Role Permissions
│   ├── academics/                # Departments, Courses, Subjects, Class Sections
│   ├── students/                 # Student Profiles, Enrollments, ID Generator
│   ├── teachers/                 # Faculty Profiles & Subject Allocations
│   ├── attendance/               # Session Attendance Logging & Percentage Engine
│   ├── examinations/             # Exam Scheduling, Results & Automated Grading
│   ├── assignments/              # Assignment Publishing & Solution Submissions
│   ├── fees/                     # Fee Structures (₹ INR), Payments & Receipts
│   ├── notices/                  # Targeted Campus Notice Board Engine
│   ├── dashboard/                # Role-Based Analytical Dashboard Views
│   └── audit/                    # System Activity & Security Audit Logger
│
├── config/                       # Central Project Settings & Global Routing
│   ├── settings.py               # Django Settings & DB Configuration
│   └── urls.py                   # URL Router & Swagger OpenAPI Endpoints
│
├── docs/                         # Comprehensive Architecture & Interview Docs
│   ├── architecture.md           # System Design & ER Diagrams
│   ├── interview-preparation.md  # Q&A for Technical Interviews
│   └── portfolio.md              # Live Interview Presentation Walkthrough
│
├── static/                       # CSS Stylesheets, JS Scripts, Icons
├── templates/                    # Modular Bootstrap 5 HTML Templates
├── manage.py                     # Django CLI Management Script
├── requirements.txt              # Python Dependencies List
└── README.md                     # Project Documentation
```

### High-Level System Architecture

```text
  +-----------------------------------------------------------------------+
  |                        Client Layer (Web / API)                       |
  |             (Bootstrap 5 Web UI / Postman / Mobile API)               |
  +-----------------------------------+-----------------------------------+
                                      |
                           HTTP / REST API Requests
                                      |
                                      v
  +-----------------------------------+-----------------------------------+
  |                       Django Routing Gateway                          |
  |                (URL Router + Auth & RBAC Middleware)                  |
  +-----------------+-----------------------------------+-----------------+
                    |                                   |
                    v                                   v
  +-----------------+-----------------+  +--------------+-----------------+
  |    Web UI Server-Side Views       |  |   DRF REST API Controllers       |
  |    (Django Templates & Forms)     |  |   (Serializers & ViewSets)       |
  +-----------------+-----------------+  +--------------+-----------------+
                    |                                   |
                    +-----------------+-----------------+
                                      |
                                      v
  +-----------------------------------+-----------------------------------+
  |                     Domain Business Logic / ORM                       |
  |      (Attendance Engine, Grading Rules, Fee Balance Calculator)       |
  +-----------------------------------+-----------------------------------+
                                      |
                                SQL Queries
                                      |
                                      v
  +-----------------------------------+-----------------------------------+
  |                  Relational Database Storage                          |
  |            (PostgreSQL / MySQL / SQLite3 DB Engine)                   |
  +-----------------------------------------------------------------------+
```

---

## 🚀 Quickstart & Local Setup Guide

Follow these simple steps to run **StudentHub** on your local machine:

### 1. Prerequisites
- **Python 3.11+** installed on your system
- **Git** version control tool

### 2. Clone Repository & Setup Virtual Environment
```bash
# Clone the repository
git clone https://github.com/your-username/studenthub.git
cd studenthub

# Create a virtual environment
python -m venv venv

# Activate virtual environment
# On Windows (PowerShell / CMD):
venv\Scripts\activate
# On Linux / macOS:
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Database Setup & Seed Demo Data
```bash
# Apply migrations to create database schema
python manage.py makemigrations
python manage.py migrate

# Seed database with realistic Indian student demo accounts & academic data
python manage.py seed_data
```

### 5. Run Development Server
```bash
python manage.py runserver
```
Visit **`http://127.0.0.1:8000/`** in your browser to access the application portal.

---

## 📖 OpenAPI / Swagger REST API Documentation

StudentHub includes auto-generated, interactive **OpenAPI 3.0 Documentation**:

- 🚀 **Swagger UI (Interactive API Tester)**: `http://127.0.0.1:8000/api/docs/`
- 📘 **ReDoc Interface**: `http://127.0.0.1:8000/api/redoc/`
- 📄 **Raw OpenAPI Schema**: `http://127.0.0.1:8000/api/schema/`

### Primary REST API Endpoints Overview

| App Domain | HTTP Method | Endpoint Path | Description |
|---|---|---|---|
| **Auth** | `POST` | `/accounts/api/auth/login/` | Obtain JWT Access & Refresh Tokens |
| **Auth** | `POST` | `/accounts/api/auth/refresh/` | Refresh Expired Access Token |
| **Academics** | `GET` / `POST` | `/academics/api/departments/` | Manage Institution Departments |
| **Academics** | `GET` / `POST` | `/academics/api/courses/` | Manage Degree Courses & Programs |
| **Students** | `GET` / `POST` | `/students/api/students/` | List & Register Enrolled Students |
| **Students** | `GET` | `/students/api/students/{id}/` | Retrieve Detailed Student Profile |
| **Attendance**| `GET` / `POST` | `/attendance/api/sessions/` | Log Session Attendance Records |
| **Attendance**| `GET` | `/attendance/api/warnings/` | Fetch Low-Attendance Flagged Students |
| **Exams** | `GET` / `POST` | `/examinations/api/results/` | Record & Query Exam Marks |
| **Fees** | `GET` | `/fees/api/balances/` | Query Student Outstanding Fee Balances |
| **Notices** | `GET` | `/notices/api/active/` | Retrieve Active Target Announcements |

---

## 🧪 Automated Testing & Quality Assurance

Run the built-in unit and integration test suite to verify code integrity:

```bash
# Execute unit tests
python manage.py test

# Execute tests for a specific domain app (e.g. students)
python manage.py test apps.students
```

---

## 💼 Highlights for Recruiters & Hiring Managers

Why **StudentHub** demonstrates strong engineering practices:

- 🛡️ **Production Security**: Implements custom permission classes, token-based REST authentication, CSRF protection, and sanitized inputs.
- ⚡ **Database Efficiency**: Optimized ORM queries using `select_related` and `prefetch_related` to eliminate N+1 query problems.
- 📐 **Clean Architecture**: Follows Single Responsibility and separation of concerns across domain-driven `apps/` layout.
- 📄 **API Standardization**: Clean OpenAPI schemas for seamless integration with frontend frameworks (React, Angular, Vue, or Mobile Apps).
- 🇮🇳 **Real-World Localization**: Fee module tailored to Indian Rupee (`₹ / INR`) currency standards and regional student datasets.

---

## 📄 License & Contact

Distributed under the **MIT License**. See `LICENSE` for details.

Developed with ❤️ by **D. Jahid Basha**.
- 💼 **GitHub**: `github.com/jahid3145`
- 📧 **Email**: `jahidbasha3145@gmail.com`

---
*If you find this project helpful for learning or recruiting evaluations, please consider giving it a ⭐️ star on GitHub!*
