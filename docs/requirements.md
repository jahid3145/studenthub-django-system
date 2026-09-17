# StudentHub — Requirements & Specifications

## 1. Executive Overview
**StudentHub** is an end-to-end Student Management & Academic Administration System engineered using Python, Django, Django REST Framework (DRF), and modern web technologies. Designed for small-to-medium educational institutions (colleges, institutes, coaching centers), StudentHub streamlines administrative operations, academic tracking, user management, and reporting.

---

## 2. Target Roles & Permission Matrix

### 2.1 Roles
1. **Super Admin**: Complete institution control, user account provisioning, system settings, department & course management, high-level reporting.
2. **Admin / Staff**: Operational administration including student enrollment, fee tracking, notice publishing, document verification, exam scheduling.
3. **Teacher**: Subject & class management, attendance recording, grade/mark entry, assignment management, notice publishing for assigned classes.
4. **Student**: View personal profile, view enrolled subjects & schedule, submit assignments, track attendance, check grades/results, view fee status, access notices.

### 2.2 Permissions Matrix

| Feature / Action | Super Admin | Admin / Staff | Teacher | Student |
|---|---|---|---|---|
| User & Role Management | Full | Read Only | None | None |
| Department & Course Setup | Full | Read/Write | Read Only | Read Only |
| Student & Teacher Profiles | Full | Full | Read Assigned | Self Only |
| Subject & Class Assignment | Full | Full | Read Assigned | Read Enrolled |
| Mark Attendance | Full | Full | Assigned Classes | View Self |
| Exam & Grade Entry | Full | Full | Assigned Subjects | View Self |
| Create Assignments | Full | Staff Only | Yes | Submit Only |
| Fee Management & Billing | Full | Full | None | View Self |
| System Audit Logs | Read Only | None | None | None |

---

## 3. Core Modules & Feature Breakdown

### 3.1 Accounts & Authentication (`apps/accounts`)
- Custom `User` model extending `AbstractUser`.
- Role-based permissions (Super Admin, Staff, Teacher, Student).
- JWT Authentication (`SimpleJWT`) for REST APIs with Access & Refresh tokens.
- Secure Session-based Auth for Web Frontend.
- Password change, reset, and validation.

### 3.2 Academics (`apps/academics`)
- **Department**: Code, Name, HOD (Teacher FK), Description, Status.
- **Course**: Name, Code, Department FK, Duration Years, Description, Status.
- **Subject**: Name, Code, Course FK, Semester, Credits, Assigned Teacher FK.
- **AcademicYear**: Code (e.g., 2025-2026), Start Date, End Date, Is Active.
- **Class / Section**: Name (e.g., CSE-3A), Course FK, Semester, Academic Year FK.

### 3.3 Student Management (`apps/students`)
- **StudentProfile**: User OneToOne, Student ID (unique string format e.g., `STU-2026-001`), Department, Course, Current Semester, Gender, DOB, Phone, Address, Admission Date, Guardian details, Photo.
- **Enrollment**: Student FK, Class FK, Academic Year FK, Semester, Status (Active, Graduated, Suspended).
- **StudentDocument**: Student Profile FK, Document Title, Document Type, File Upload, Verification Status.

### 3.4 Teacher Management (`apps/teachers`)
- **TeacherProfile**: User OneToOne, Employee ID (unique string format e.g., `EMP-2026-001`), Department, Designation, Qualification, Joining Date, Phone, Address, Photo.

### 3.5 Attendance System (`apps/attendance`)
- **Attendance Session / Header**: Subject FK, Class FK, Date, Marked By (Teacher FK).
- **Attendance Record**: Student FK, Session FK, Status (Present, Absent, Late, Excused), Remarks.
- **Rules**: Prevent duplicate attendance for the same subject/class/date. Attendance percentage calculation formula: `(Present / Total) * 100`. Low attendance threshold alert (`< 75%`).

### 3.6 Examination & Marks (`apps/examinations`)
- **Exam**: Title, Exam Type (Internal, Mid-Term, Final, Quiz), Academic Year, Start Date, End Date.
- **ExamSchedule**: Exam FK, Subject FK, Class FK, Date, Max Marks, Passing Marks.
- **ExamResult**: Student FK, Exam Schedule FK, Marks Obtained, Grade, Remarks, Entered By (Teacher FK).
- Automatic calculation of total percentage, grade point, letter grade (A+, A, B+, B, C, D, F), and Pass/Fail status.

### 3.7 Assignments (`apps/assignments`)
- **Assignment**: Title, Description, Subject FK, Class FK, Created By (Teacher FK), Due Date, Max Marks, Attachment.
- **AssignmentSubmission**: Assignment FK, Student FK, Submitted File, Text Submission, Submitted At, Status (Submitted, Late, Graded), Marks, Feedback.

### 3.8 Fee Management (`apps/fees`)
- **FeeStructure**: Course FK, Academic Year FK, Semester, Fee Category (Tuition, Exam, Library, Admission), Total Amount, Due Date.
- **StudentFee**: Student FK, Fee Structure FK, Discount, Final Amount, Paid Amount, Due Amount, Status (Paid, Partial, Unpaid, Overdue).
- **PaymentRecord**: Student Fee FK, Payment Reference / Txn ID, Amount Paid, Payment Date, Payment Method (Cash, Bank Transfer, Online Simulation), Status.

### 3.9 Notices & Announcements (`apps/notices`)
- **Notice**: Title, Content, Created By (User FK), Target Audience (All, Department, Course, Class), Attachment, Created At, Expiry Date, Priority (Low, Normal, Urgent).

### 3.10 System Audit & Dashboards (`apps/dashboard` & `apps/audit`)
- **AuditLog**: User FK, Action (Create, Update, Delete, Login), Model Name, Record ID, Description, Timestamp, IP Address.
- Role-Tailored Interactive Dashboards for Admin, Teacher, and Student with KPI summary cards, quick actions, charts, and activity feeds.

---

## 4. Technical Non-Functional Requirements
- **PEP 8 Compliance**: Strict python formatting standards.
- **Security**: CSRF protection on forms, JWT for APIs, SQL injection prevention via Django ORM, secure file validation for uploads, CORS control.
- **Database Efficiency**: Proper index usage, explicit `select_related` and `prefetch_related` on relational queries to eliminate N+1 issues.
- **Error Handling & Response Standardization**: Uniform JSON structure `{ success, message, data, errors }` across DRF endpoints.
- **API Documentation**: OpenAPI / Swagger generation via `drf-spectacular`.
- **Environment Isolation**: `.env` configuration for sensitive settings (`SECRET_KEY`, `DEBUG`, `DATABASE_URL`).
