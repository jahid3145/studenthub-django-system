# StudentHub — Interview Preparation Guide

This guide prepares a candidate for technical interview discussions around the **StudentHub** application.

---

## 1. Project Overview & Elevator Pitch
> *"I built **StudentHub**, a full-stack Student Management & Academic Administration System designed for educational institutions. It features dual-mode architecture: a responsive Bootstrap 5 Web UI for administration and academic management, alongside a REST API built with Django REST Framework (DRF), JWT authentication, Swagger UI, and PostgreSQL."*

---

## 2. Technical Q&A for Fresher / Junior Interviews

### Q1: Why did you choose Django and Django REST Framework?
**Answer**: Django provides a robust, battery-included framework with a built-in ORM, security against common web vulnerabilities (CSRF, SQL Injection, XSS), and an administrative panel out of the box. DRF extends Django to allow declarative API development using serializers, viewsets, permission classes, and OpenAPI schema generators (`drf-spectacular`).

### Q2: Why PostgreSQL instead of SQLite or MySQL?
**Answer**: PostgreSQL is enterprise-grade, highly reliable, and supports ACID compliance, complex relational integrity, spatial data, and concurrent read-write scaling. While SQLite is useful for initial local prototyping, PostgreSQL represents production standards.

### Q3: How does JWT Authentication work in StudentHub?
**Answer**: We use `djangorestframework-simplejwt`. Upon posting valid credentials to `/accounts/api/auth/login/`, the server returns an **Access Token** (short-lived, 60 minutes) and a **Refresh Token** (long-lived, 24 hours). Clients attach the Access Token in the request header: `Authorization: Bearer <access_token>`.

### Q4: How is Role-Based Access Control (RBAC) enforced?
**Answer**: We extended Django's `AbstractUser` with a custom `role` field containing choices (`SUPERADMIN`, `ADMIN`, `TEACHER`, `STUDENT`). We created custom DRF permissions (`IsAdminOrStaff`, `IsTeacher`, `IsStudent`, `IsOwnerOrAdmin`) to wrap API viewsets.

### Q5: How did you prevent a student from accessing another student's data?
**Answer**: We enforced scope isolation in two places:
1. **Queryset Level**: In `StudentProfileViewSet.get_queryset()`, if `user.is_student`, the query filters `StudentProfile.objects.filter(user=user)`.
2. **Object Level Permission**: `IsOwnerOrAdmin` verifies `obj.user == request.user` before serving data.

### Q6: How does Attendance Percentage calculation work?
**Answer**: 
$$\text{Attendance } \% = \left(\frac{\text{Present + Late Sessions}}{\text{Total Sessions}}\right) \times 100$$
If the calculated percentage drops below 75.0%, the system flags an automated warning badge (`is_low_attendance_warning: true`).

### Q7: How is automated grade calculation handled?
**Answer**: In `ExamResult.save()`, we compute percentage as `(marks_obtained / max_marks) * 100`. Grades are assigned automatically:
- 90%+: `A+` (GP 10.0)
- 80-89%: `A` (GP 9.0)
- 70-79%: `B+` (GP 8.0)
- 60-69%: `B` (GP 7.0)
- 50-59%: `C` (GP 6.0)
- 40-49%: `D` (GP 5.0)
- <40%: `F` (GP 0.0, Fail)

### Q8: What database query optimizations did you apply?
**Answer**: We avoided N+1 query overhead by using `select_related()` for single-valued relationships (e.g. `user`, `department`, `course`) and `prefetch_related()` for multi-valued relationships (e.g. `assigned_subjects`, `payments`).
