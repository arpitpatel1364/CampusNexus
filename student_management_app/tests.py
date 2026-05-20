from django.test import TestCase, Client
from django.urls import reverse
from student_management_app.models import CustomUser, Courses, SessionYearModel, Students, Staffs, AdminHOD
import datetime


class StudentManagementTests(TestCase):
    def setUp(self):
        self.client = Client()
        # Create a course and session year for testing profile association
        self.session_year = SessionYearModel.objects.create(
            session_start_year=datetime.date(2026, 1, 1),
            session_end_year=datetime.date(2026, 12, 31)
        )
        self.course = Courses.objects.create(course_name="Computer Science")

    def test_student_self_registration_and_login(self):
        # 1. Register a student via POST
        response = self.client.post(reverse('doRegistration'), {
            'first_name': 'Test',
            'last_name': 'Student',
            'email': 'johndoe.student@college.edu',
            'password': 'password123',
            'confirmPassword': 'password123'
        })
        self.assertEqual(response.status_code, 200)  # Renders login page

        # Verify CustomUser and Students objects were created
        user = CustomUser.objects.get(email='johndoe.student@college.edu')
        self.assertEqual(user.first_name, 'Test')
        self.assertEqual(user.last_name, 'Student')
        self.assertEqual(user.user_type, '3')
        
        # Verify student profile exists (created by post_save signal)
        self.assertTrue(hasattr(user, 'students'))
        self.assertIsNone(user.students.course_id)  # Null initially since it is self-registered

        # 2. Log in the student
        response = self.client.post(reverse('doLogin'), {
            'email': 'johndoe.student@college.edu',
            'password': 'password123'
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/student_home/')

        # 3. Access student home (should render successfully)
        response = self.client.get('/student_home/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Course Enrollment Pending")

    def test_staff_login_and_home(self):
        # 1. Create a staff user directly (similar to how HOD does it)
        user = CustomUser.objects.create_user(
            username='staff_member',
            email='staff.staff@college.edu',
            password='password123',
            user_type='2'
        )
        self.assertTrue(hasattr(user, 'staffs'))

        # 2. Log in the staff
        response = self.client.post(reverse('doLogin'), {
            'email': 'staff.staff@college.edu',
            'password': 'password123'
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/staff_home/')

    def test_hod_login_and_home(self):
        # 1. Create an HOD user directly
        user = CustomUser.objects.create_user(
            username='hod_member',
            email='hod.hod@college.edu',
            password='password123',
            user_type='1'
        )
        self.assertTrue(hasattr(user, 'adminhod'))

        # 2. Log in the HOD
        response = self.client.post(reverse('doLogin'), {
            'email': 'hod.hod@college.edu',
            'password': 'password123'
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/admin_home/')
