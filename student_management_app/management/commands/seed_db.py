import datetime
import random
from django.core.management.base import BaseCommand
from django.core.management import call_command
from student_management_app.models import (
    CustomUser, Courses, SessionYearModel, Subjects, 
    Students, Staffs, Attendance, AttendanceReport, 
    LeaveReportStudent, LeaveReportStaff, StudentResult
)

class Command(BaseCommand):
    help = 'Automates database migration, default Admin creation, and seeds 200 students and 20 staff members with realistic attendance and leave data.'

    def handle(self, *args, **kwargs):
        self.stdout.write('Step 1: Running migrations...')
        call_command('makemigrations')
        call_command('migrate')

        self.stdout.write('Step 2: Clearing old institution structure and transactional data...')
        StudentResult.objects.all().delete()
        LeaveReportStudent.objects.all().delete()
        LeaveReportStaff.objects.all().delete()
        AttendanceReport.objects.all().delete()
        Attendance.objects.all().delete()
        
        # Unlink students to avoid FOREIGN KEY violations during course deletion
        Students.objects.all().update(course_id=None, session_year_id=None)
        Subjects.objects.all().delete()
        Courses.objects.all().delete()

        self.stdout.write('Step 3: Creating session year and courses...')
        session, _ = SessionYearModel.objects.get_or_create(
            id=1,
            defaults={
                'session_start_year': datetime.date(2026, 1, 1),
                'session_end_year': datetime.date(2026, 12, 31)
            }
        )

        course_names = [
            'Computer Science',
            'Information Technology',
            'Electronics Engineering',
            'Mechanical Engineering',
            'Civil Engineering'
        ]
        courses = []
        for name in course_names:
            c = Courses.objects.create(course_name=name)
            courses.append(c)

        self.stdout.write('Step 4: Ensuring Admin, Staff, and Student accounts exist...')
        # Admin / HOD
        admin_user = CustomUser.objects.filter(username='admin').first() or CustomUser.objects.filter(email='admin@example.com').first()
        if admin_user:
            admin_user.username = 'admin'
            admin_user.email = 'admin@example.com'
            admin_user.set_password('adminpassword123')
            admin_user.user_type = '1'
            admin_user.save()
        else:
            CustomUser.objects.create_user(
                username='admin',
                email='admin@example.com',
                password='adminpassword123',
                user_type='1',
                first_name='Admin',
                last_name='User'
            )

        # 20 Staff Users
        staff_users = list(CustomUser.objects.filter(user_type='2'))
        for i in range(len(staff_users) + 1, 21):
            u = CustomUser.objects.create_user(
                username=f'staff{i}',
                email=f'staff{i}.staff@college.edu',
                password='password123',
                user_type='2',
                first_name=f'StaffFirst{i}',
                last_name=f'StaffLast{i}'
            )
            staff_users.append(u)

        # 200 Students
        student_users = list(CustomUser.objects.filter(user_type='3'))
        for i in range(len(student_users) + 1, 201):
            u = CustomUser.objects.create_user(
                username=f'student{i}',
                email=f'student{i}.student@college.edu',
                password='password123',
                user_type='3',
                first_name=f'StudentFirst{i}',
                last_name=f'StudentLast{i}'
            )
            student_users.append(u)

        self.stdout.write('Step 5: Setting up subjects and teacher assignments...')
        subjects_data = {
            'Computer Science': ['Data Structures', 'Algorithms', 'Databases'],
            'Information Technology': ['Web Technology', 'Software Testing', 'Cyber Security'],
            'Electronics Engineering': ['Embedded Systems', 'Circuit Design', 'Digital Signal Processing'],
            'Mechanical Engineering': ['Thermodynamics', 'Fluid Mechanics', 'CAD Design'],
            'Civil Engineering': ['Structural Design', 'Concrete Technology', 'Surveying']
        }

        all_subjects = []
        staff_idx = 0
        for course_obj in courses:
            c_name = course_obj.course_name
            sub_names = subjects_data[c_name]
            for s_name in sub_names:
                assigned_staff = staff_users[staff_idx % len(staff_users)]
                staff_idx += 1
                sub = Subjects.objects.create(
                    subject_name=s_name,
                    course_id=course_obj,
                    staff_id=assigned_staff
                )
                all_subjects.append(sub)

        self.stdout.write('Step 6: Enrolling students to courses...')
        for idx, s_user in enumerate(student_users):
            course_assigned = courses[idx % len(courses)]
            profile = s_user.students
            profile.course_id = course_assigned
            profile.session_year_id = session
            profile.gender = 'Male' if idx % 2 == 0 else 'Female'
            profile.address = f'Hostel Room {idx + 1}'
            profile.save()

        self.stdout.write('Step 7: Seeding daily attendance history...')
        attendance_dates = [
            datetime.date(2026, 5, 1) + datetime.timedelta(days=d) 
            for d in range(10)
        ]

        for sub in all_subjects:
            students_in_course = Students.objects.filter(course_id=sub.course_id)
            for a_date in attendance_dates:
                att = Attendance.objects.create(
                    subject_id=sub,
                    attendance_date=a_date,
                    session_year_id=session
                )
                reports = []
                for student_profile in students_in_course:
                    status = random.random() < 0.85
                    reports.append(AttendanceReport(
                        student_id=student_profile,
                        attendance_id=att,
                        status=status
                    ))
                AttendanceReport.objects.bulk_create(reports)

        self.stdout.write('Step 8: Seeding leave applications...')
        # Staff leaves
        for u in staff_users:
            if random.random() < 0.6:
                num_leaves = random.randint(1, 3)
                for l_idx in range(num_leaves):
                    LeaveReportStaff.objects.create(
                        staff_id=u.staffs,
                        leave_date=f'2026-05-{random.randint(10, 28)}',
                        leave_message=f'Personal emergency {l_idx + 1}',
                        leave_status=random.choice([0, 1, 2])
                    )

        # Student leaves (first 50)
        for u in student_users[:50]:
            if random.random() < 0.4:
                num_leaves = random.randint(1, 2)
                for l_idx in range(num_leaves):
                    LeaveReportStudent.objects.create(
                        student_id=u.students,
                        leave_date=f'2026-05-{random.randint(10, 28)}',
                        leave_message=f'Health issue {l_idx + 1}',
                        leave_status=random.choice([0, 1, 2])
                    )

        self.stdout.write(self.style.SUCCESS('Successfully migrated and seeded all CampusNexus data!'))
