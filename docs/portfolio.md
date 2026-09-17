# StudentHub — Portfolio & Interview Demo Flow

This guide outlines how to present **StudentHub** on GitHub, portfolio websites, and live technical interviews.

---

## 1. Professional Demo Walkthrough (5–10 Minutes)

1. **Introduction (1 min)**:
   - Present the project objective: *StudentHub* streamlines administrative workflows for colleges & institutes.
   - Explain dual architecture: Web UI + DRF REST API with Swagger documentation.

2. **Super Admin Dashboard (2 mins)**:
   - Log in as `admin` (`Admin@123`).
   - Showcase institution KPIs (Total Students, Teachers, Departments, Fee Collected).
   - Demonstrate Academic management: Departments (CSE, ECE), Courses, Subjects, and Class Sections.

3. **Faculty / Teacher Portal (2 mins)**:
   - Log in as `prof.sharma` (`Teacher@123`).
   - Show assigned subjects (Data Structures, DBMS).
   - Demonstrate attendance tracking and exam grade submission.

4. **Student Portal (2 mins)**:
   - Log in as `rahul.kumar` (`Student@123`).
   - Highlight student attendance percentage meter & low-attendance alert.
   - Showcase academic transcript, fee balance, and campus announcements.

5. **REST API & Swagger Documentation (2 mins)**:
   - Navigate to `/api/docs/`.
   - Test JWT authentication endpoint `/accounts/api/auth/login/`.
   - Authorize Swagger UI with JWT Bearer Token and test `/students/api/students/` API endpoint.

6. **Code Architecture & Database Schema (1 min)**:
   - Walk through modular `apps/` layout, custom User model, ORM query optimizations, and unit test suite.
