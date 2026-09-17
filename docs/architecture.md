# StudentHub — System Architecture & Design Document

## 1. High-Level System Architecture

```
                                  +---------------------------------------+
                                  |            Web Browser / Client       |
                                  |  (Bootstrap 5 / Modern CSS / JS API)  |
                                  +-------------------+-------------------+
                                                      |
                                          HTTP / HTTPS / REST API
                                                      |
                                                      v
                                  +-------------------+-------------------+
                                  |        Django Application Gateway     |
                                  |     (Config / Security / Routing)     |
                                  +---------+-------------------+---------+
                                            |                   |
                     +----------------------+                   +----------------------+
                     |                                                                 |
                     v                                                                 v
        +------------+------------+                                       +------------+------------+
        |   Django Server Templates|                                       |   DRF REST API Controllers|
        |   (SSR Views + Forms)   |                                       |   (Serializers + ViewSets)|
        +------------+------------+                                       +------------+------------+
                     |                                                                 |
                     +----------------------+                   +----------------------+
                                            |                   |
                                            v                   v
                                  +---------+-------------------+---------+
                                  |       Domain Service Layer / ORM      |
                                  |       (Business Logic / Analytics)    |
                                  +-------------------+-------------------+
                                                      |
                                        SQL Queries / Connections
                                                      |
                                                      v
                                  +-------------------+-------------------+
                                  |    MySQL / PostgreSQL Relational DB|
                                  |  (Users, Students, Marks, Fees, etc.) |
                                  +---------------------------------------+
```

---

## 2. Django Modular App Breakdown

1. `apps.accounts`: Custom user authentication model, JWT views, profile base, role permissions, custom permission classes.
2. `apps.academics`: Department, Course, Subject, AcademicYear, and Class models, views, API endpoints.
3. `apps.students`: Student profiles, enrollments, student document uploads, student API endpoints.
4. `apps.teachers`: Teacher profiles, subject teacher assignments, teacher API endpoints.
5. `apps.attendance`: Attendance header & detail records, attendance percentage calculation service, warnings API.
6. `apps.examinations`: Exams, exam schedules, exam results, automated grading service, result management API.
7. `apps.assignments`: Assignments, student submissions, file handling, grading feedback API.
8. `apps.fees`: Fee structure, student fee balances, payment transactions, receipt generation data.
9. `apps.notices`: Notices, target audience filtering engine, active announcements API.
10. `apps.dashboard`: Consolidated analytics for Admin, Teacher, and Student roles.
11. `apps.audit`: Centralized system audit logger.

---

## 3. Database Entity-Relationship Summary

```
                       +-------------------+
                       |    Custom User    |
                       | (Role, Email, ID) |
                       +---------+---------+
                                 |
              +------------------+------------------+
             1|                                    1|
              v                                     v
    +---------+---------+                 +---------+---------+
    |  TeacherProfile   |                 |  StudentProfile   |
    +----+--------------+                 +----+--------------+
         |                                     |
         | * assigned to                       | * enrolled in
         v                                     v
    +----+--------------+                 +----+--------------+
    |      Subject      |                 |    Enrollment     |
    +----+--------------+                 +----+--------------+
         |                                     |
         | * has                               | * belongs to
         v                                     v
    +----+--------------+                 +----+--------------+
    |   Attendance /    |                 |   Class / Section |
    |   Exam Schedule   |                 +-------------------+
    +----+--------------+
         |
         | * records
         v
    +----+--------------+
    | ExamResult / Mark |
    +-------------------+
```

---

## 4. REST API Standard Response Format

All REST API endpoints implement a standard envelope pattern:

### Success Response (200 OK / 201 Created)
```json
{
  "success": true,
  "message": "Operation completed successfully.",
  "data": { ... },
  "errors": null
}
```

### Error Response (400 Bad Request / 401 Unauthorized / 403 Forbidden / 404 Not Found)
```json
{
  "success": false,
  "message": "Validation or execution error message.",
  "data": null,
  "errors": {
    "field_name": ["Specific validation error message."]
  }
}
```

---

## 5. Technology Stack Rationale (Fresher Interview Explainability)

- **Python 3.11+ & Django 5.x**: Industry-standard high-level web framework providing built-in ORM, security, form handling, and administrative panel out of the box.
- **Django REST Framework (DRF)**: Premier API framework for Django providing serialization, generic views, authentication wrappers, and OpenAPI integration.
- **PostgreSQL**: Production-grade relational database management system supporting ACID compliance, complex foreign keys, indexing, and scalable transactions.
- **SimpleJWT**: Lightweight JSON Web Token authentication standard providing secure stateless authorization headers for mobile and web REST clients.
- **django-filter & drf-spectacular**: Provides declarative query-parameter filtering and auto-generated Swagger UI documentation without bloat.
- **Bootstrap 5 & Vanilla JS**: Clean, responsive frontend styling and light interactivity without complex SPA build tooling overhead.
