from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import date, timedelta

from apps.academics.models import Department, Course, Subject, AcademicYear, ClassSection
from apps.teachers.models import TeacherProfile
from apps.students.models import StudentProfile, Enrollment
from apps.attendance.models import AttendanceSession, AttendanceRecord
from apps.examinations.models import Exam, ExamSchedule, ExamResult
from apps.assignments.models import Assignment, AssignmentSubmission
from apps.fees.models import FeeStructure, StudentFee, PaymentRecord
from apps.notices.models import Notice

User = get_user_model()


class Command(BaseCommand):
    help = 'Seeds database with realistic institution demo data for testing & interviews.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("Starting StudentHub database seeding..."))

        # Clean up existing student users to avoid duplicate student_id collisions when re-seeding
        User.objects.filter(role=User.Role.STUDENT).delete()

        # 1. Create Users
        admin_user, _ = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@studenthub.edu',
                'first_name': 'Super',
                'last_name': 'Admin',
                'role': User.Role.SUPERADMIN,
                'is_staff': True,
                'is_superuser': True
            }
        )
        admin_user.set_password('Admin@123')
        admin_user.save()

        staff_user, _ = User.objects.get_or_create(
            username='staff1',
            defaults={
                'email': 'staff@studenthub.edu',
                'first_name': 'Karan',
                'last_name': 'Mehta',
                'role': User.Role.ADMIN,
                'is_staff': True
            }
        )
        staff_user.set_password('Staff@123')
        staff_user.save()

        # Teachers
        t1_user, _ = User.objects.get_or_create(
            username='prof.sharma',
            defaults={
                'email': 'sharma@studenthub.edu',
                'first_name': 'Rajesh',
                'last_name': 'Sharma',
                'role': User.Role.TEACHER
            }
        )
        t1_user.set_password('Teacher@123')
        t1_user.save()

        t2_user, _ = User.objects.get_or_create(
            username='prof.patel',
            defaults={
                'email': 'patel@studenthub.edu',
                'first_name': 'Ananya',
                'last_name': 'Patel',
                'role': User.Role.TEACHER
            }
        )
        t2_user.set_password('Teacher@123')
        t2_user.save()

        # Students Data List (15 Enrolled Indian Students)
        student_data = [
            {'username': 'd.jahidbasha', 'email': 'jahid.basha@example.com', 'first_name': 'D. Jahid', 'last_name': 'Basha', 'dept_code': 'CSE', 'sem': 3, 'gender': 'M', 'phone': '+91 9876543201', 'guardian': 'Dawud Basha'},
            {'username': 'k.hussain', 'email': 'hussain.k@example.com', 'first_name': 'K.', 'last_name': 'Hussain', 'dept_code': 'ECE', 'sem': 3, 'gender': 'M', 'phone': '+91 9876543202', 'guardian': 'Khadar Basha'},
            {'username': 'b.indra', 'email': 'indra.b@example.com', 'first_name': 'B.', 'last_name': 'Indra', 'dept_code': 'CSE', 'sem': 3, 'gender': 'M', 'phone': '+91 9876543203', 'guardian': 'B. Bhaskar'},
            {'username': 'narasimha', 'email': 'narasimha@example.com', 'first_name': 'Narasimha', 'last_name': 'Rao', 'dept_code': 'ECE', 'sem': 3, 'gender': 'M', 'phone': '+91 9876543204', 'guardian': 'Venkateswara Rao'},
            {'username': 'kiran', 'email': 'kiran@example.com', 'first_name': 'Kiran', 'last_name': 'Kumar', 'dept_code': 'CSE', 'sem': 3, 'gender': 'M', 'phone': '+91 9876543205', 'guardian': 'Ramanjaneyulu'},
            {'username': 'rahul.kumar', 'email': 'rahul@example.com', 'first_name': 'Rahul', 'last_name': 'Kumar', 'dept_code': 'CSE', 'sem': 3, 'gender': 'M', 'phone': '+91 9876543210', 'guardian': 'Suresh Kumar'},
            {'username': 'priya.singh', 'email': 'priya@example.com', 'first_name': 'Priya', 'last_name': 'Singh', 'dept_code': 'ECE', 'sem': 3, 'gender': 'F', 'phone': '+91 9876543211', 'guardian': 'Ramesh Singh'},
            {'username': 'aarav.sharma', 'email': 'aarav@example.com', 'first_name': 'Aarav', 'last_name': 'Sharma', 'dept_code': 'CSE', 'sem': 3, 'gender': 'M', 'phone': '+91 9876543212', 'guardian': 'Vijay Sharma'},
            {'username': 'ananya.verma', 'email': 'ananya@example.com', 'first_name': 'Ananya', 'last_name': 'Verma', 'dept_code': 'CSE', 'sem': 3, 'gender': 'F', 'phone': '+91 9876543213', 'guardian': 'Alok Verma'},
            {'username': 'rohan.gupta', 'email': 'rohan@example.com', 'first_name': 'Rohan', 'last_name': 'Gupta', 'dept_code': 'ECE', 'sem': 3, 'gender': 'M', 'phone': '+91 9876543214', 'guardian': 'Sunil Gupta'},
            {'username': 'sneha.reddy', 'email': 'sneha@example.com', 'first_name': 'Sneha', 'last_name': 'Reddy', 'dept_code': 'CSE', 'sem': 3, 'gender': 'F', 'phone': '+91 9876543215', 'guardian': 'Venkat Reddy'},
            {'username': 'vikram.patel', 'email': 'vikram@example.com', 'first_name': 'Vikram', 'last_name': 'Patel', 'dept_code': 'ECE', 'sem': 3, 'gender': 'M', 'phone': '+91 9876543216', 'guardian': 'Dinesh Patel'},
            {'username': 'ishita.joshi', 'email': 'ishita@example.com', 'first_name': 'Ishita', 'last_name': 'Joshi', 'dept_code': 'CSE', 'sem': 3, 'gender': 'F', 'phone': '+91 9876543217', 'guardian': 'Mahesh Joshi'},
            {'username': 'aditya.nair', 'email': 'aditya@example.com', 'first_name': 'Aditya', 'last_name': 'Nair', 'dept_code': 'ECE', 'sem': 3, 'gender': 'M', 'phone': '+91 9876543218', 'guardian': 'Kishore Nair'},
            {'username': 'kavya.deshmukh', 'email': 'kavya@example.com', 'first_name': 'Kavya', 'last_name': 'Deshmukh', 'dept_code': 'CSE', 'sem': 3, 'gender': 'F', 'phone': '+91 9876543219', 'guardian': 'Shantanu Deshmukh'},
        ]

        # 2. Departments & Courses
        cse_dept, _ = Department.objects.get_or_create(
            code='CSE',
            defaults={'name': 'Computer Science & Engineering', 'description': 'Department of Computer Science'}
        )
        ece_dept, _ = Department.objects.get_or_create(
            code='ECE',
            defaults={'name': 'Electronics & Communication Engineering', 'description': 'Department of Electronics'}
        )

        t1_profile, _ = TeacherProfile.objects.get_or_create(
            user=t1_user,
            defaults={'employee_id': 'EMP-2026-001', 'department': cse_dept, 'designation': 'Professor & HOD', 'qualification': 'Ph.D. in Computer Science'}
        )
        t2_profile, _ = TeacherProfile.objects.get_or_create(
            user=t2_user,
            defaults={'employee_id': 'EMP-2026-002', 'department': ece_dept, 'designation': 'Associate Professor', 'qualification': 'M.Tech in VLSI Design'}
        )

        cse_dept.head_of_department = t1_profile
        cse_dept.save()

        course_cse, _ = Course.objects.get_or_create(
            code='BTECH-CSE',
            defaults={'name': 'Bachelor of Technology in CSE', 'department': cse_dept, 'duration_years': 4, 'total_semesters': 8}
        )
        course_ece, _ = Course.objects.get_or_create(
            code='BTECH-ECE',
            defaults={'name': 'Bachelor of Technology in ECE', 'department': ece_dept, 'duration_years': 4, 'total_semesters': 8}
        )

        # 3. Subjects
        sub_ds, _ = Subject.objects.get_or_create(
            code='CS101',
            defaults={'name': 'Data Structures & Algorithms', 'course': course_cse, 'semester': 3, 'credits': 4, 'teacher': t1_profile}
        )
        sub_db, _ = Subject.objects.get_or_create(
            code='CS102',
            defaults={'name': 'Database Management Systems', 'course': course_cse, 'semester': 3, 'credits': 4, 'teacher': t1_profile}
        )

        # 4. Academic Year & Classes
        curr_year, _ = AcademicYear.objects.get_or_create(
            name='2025-2026',
            defaults={'start_date': date(2025, 8, 1), 'end_date': date(2026, 6, 30), 'is_current': True}
        )

        class_cse3a, _ = ClassSection.objects.get_or_create(
            name='CSE-3A',
            academic_year=curr_year,
            semester=3,
            defaults={'course': course_cse, 'capacity': 60}
        )

        class_ece3a, _ = ClassSection.objects.get_or_create(
            name='ECE-3A',
            academic_year=curr_year,
            semester=3,
            defaults={'course': course_ece, 'capacity': 60}
        )

        # 5. Student Profiles & Enrollments Loop
        dept_map = {'CSE': cse_dept, 'ECE': ece_dept}
        course_map = {'CSE': course_cse, 'ECE': course_ece}
        class_map = {'CSE': class_cse3a, 'ECE': class_ece3a}
        
        student_profiles = []
        for i, s_data in enumerate(student_data, start=1):
            user_obj, _ = User.objects.get_or_create(
                username=s_data['username'],
                defaults={
                    'email': s_data['email'],
                    'first_name': s_data['first_name'],
                    'last_name': s_data['last_name'],
                    'role': User.Role.STUDENT,
                    'phone': s_data['phone']
                }
            )
            user_obj.set_password('Student@123')
            user_obj.save()

            dept = dept_map[s_data['dept_code']]
            crs = course_map[s_data['dept_code']]
            cls = class_map[s_data['dept_code']]

            prof, _ = StudentProfile.objects.get_or_create(
                user=user_obj,
                defaults={
                    'student_id': f'STU-2026-{i:03d}',
                    'department': dept,
                    'course': crs,
                    'current_semester': s_data['sem'],
                    'gender': s_data['gender'],
                    'phone': s_data['phone'],
                    'guardian_name': s_data['guardian'],
                    'guardian_phone': s_data['phone'],
                    'address': f'City Hostel Block-{chr(65 + i%4)}, Tech Campus'
                }
            )
            student_profiles.append(prof)

            Enrollment.objects.get_or_create(
                student=prof,
                class_section=cls,
                academic_year=curr_year,
                defaults={'semester': s_data['sem']}
            )

        # 6. Attendance Sessions & Records
        session1, _ = AttendanceSession.objects.get_or_create(
            subject=sub_ds,
            class_section=class_cse3a,
            date=date.today() - timedelta(days=1),
            defaults={'marked_by': t1_profile}
        )
        for prof in student_profiles:
            AttendanceRecord.objects.get_or_create(session=session1, student=prof, defaults={'status': 'P'})

        # 7. Exams & Results
        mid_exam, _ = Exam.objects.get_or_create(
            name='Mid-Term 2026',
            academic_year=curr_year,
            defaults={'exam_type': 'MIDTERM', 'start_date': date.today() - timedelta(days=10), 'end_date': date.today() - timedelta(days=5), 'is_published': True}
        )
        sched1, _ = ExamSchedule.objects.get_or_create(
            exam=mid_exam,
            subject=sub_ds,
            class_section=class_cse3a,
            defaults={'exam_date': date.today() - timedelta(days=8), 'start_time': '10:00:00', 'end_time': '12:00:00', 'max_marks': 100, 'passing_marks': 40}
        )
        for prof in student_profiles[:5]:
            ExamResult.objects.get_or_create(
                student=prof,
                exam_schedule=sched1,
                defaults={'marks_obtained': 85.00, 'entered_by': t1_profile}
            )

        # 8. Fees & Payments in Indian Rupees (₹ / INR)
        fee_struct_cse, _ = FeeStructure.objects.get_or_create(
            course=course_cse,
            academic_year=curr_year,
            semester=3,
            title='B.Tech CSE Sem 3 Tuition Fee',
            defaults={'total_amount': 65000.00, 'due_date': date.today() + timedelta(days=30)}
        )
        fee_struct_ece, _ = FeeStructure.objects.get_or_create(
            course=course_ece,
            academic_year=curr_year,
            semester=3,
            title='B.Tech ECE Sem 3 Tuition Fee',
            defaults={'total_amount': 60000.00, 'due_date': date.today() + timedelta(days=30)}
        )

        for i, prof in enumerate(student_profiles):
            fs = fee_struct_cse if prof.department == cse_dept else fee_struct_ece
            disc = 5000.00 if i % 2 == 0 else 0.00
            stu_fee, _ = StudentFee.objects.get_or_create(
                student=prof,
                fee_structure=fs,
                defaults={'discount_amount': disc}
            )
            
            # Partial or full payment simulation in INR
            paid_amt = 40000.00 if i < 6 else 0.00
            if paid_amt > 0:
                PaymentRecord.objects.get_or_create(
                    student_fee=stu_fee,
                    transaction_id=f'TXN-2026-DEMO{i+1:02d}',
                    defaults={'amount': paid_amt, 'payment_method': 'ONLINE'}
                )

        # 9. Notices
        Notice.objects.get_or_create(
            title='Mid-Term Results Published',
            defaults={
                'content': 'The mid-term examination results for Semester 3 have been published. Please check your transcript portal.',
                'created_by': admin_user,
                'target_audience': 'ALL',
                'priority': 'HIGH'
            }
        )

        self.stdout.write(self.style.SUCCESS(f"Successfully seeded StudentHub database with {len(student_profiles)} students and INR fee structures!"))
