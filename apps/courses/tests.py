# ==============================================================================
# TESTS FOR COURSES APP
# تاریخ ایجاد: ۱۴۰۳/۰۶/۲۰
# ==============================================================================

from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from apps.courses.models import Course
from apps.users.models import User


class CourseModelTest(TestCase):
    """Test Course model"""

    def setUp(self):
        self.user = User.objects.create_user(
            username='professor1',
            national_id='1234567890',
            email='prof@test.com',
            password='testpass123',
            user_type='EMPLOYEE'
        )

    def test_course_creation(self):
        """Test creating a course"""
        course = Course.objects.create(
            title='Test Course',
            code='TC101',
            description='Test Description',
            professor=self.user
        )
        
        self.assertEqual(course.title, 'Test Course')
        self.assertEqual(course.code, 'TC101')
        self.assertEqual(course.professor, self.user)
        self.assertEqual(str(course), 'TC101 - Test Course')

    def test_course_student_enrollment(self):
        """Test student enrollment"""
        course = Course.objects.create(
            title='Test Course',
            code='TC101',
            professor=self.user
        )
        
        student = User.objects.create_user(
            username='student1',
            national_id='1234567891',
            email='student@test.com',
            password='testpass123',
            user_type='STUDENT'
        )
        
        course.students.add(student)
        self.assertEqual(course.students.count(), 1)
        self.assertIn(student, course.students.all())


class CourseAPITest(APITestCase):
    """Test Course API endpoints"""

    def setUp(self):
        self.client = APIClient()
        
        # Create users
        self.admin = User.objects.create_user(
            username='admin',
            national_id='1234567890',
            email='admin@test.com',
            password='testpass123',
            user_type='ADMIN'
        )
        
        self.professor = User.objects.create_user(
            username='professor',
            national_id='1234567891',
            email='prof@test.com',
            password='testpass123',
            user_type='EMPLOYEE'
        )
        
        self.student = User.objects.create_user(
            username='student',
            national_id='1234567892',
            email='student@test.com',
            password='testpass123',
            user_type='STUDENT'
        )
        
        # Create course
        self.course = Course.objects.create(
            title='Test Course',
            code='TC101',
            description='Test Description',
            professor=self.professor
        )

    def test_course_list_authenticated(self):
        """Test course list with authentication"""
        self.client.force_authenticate(user=self.admin)
        url = reverse('course-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, 'Test Course')

    def test_course_list_unauthenticated(self):
        """Test course list without authentication"""
        url = reverse('course-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_course_creation_by_admin(self):
        """Test course creation by admin"""
        self.client.force_authenticate(user=self.admin)
        url = reverse('course-list')
        
        data = {
            'title': 'New Course',
            'code': 'NC101',
            'description': 'New Course Description',
            'professor': self.professor.id
        }
        
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Course.objects.filter(code='NC101').count(), 1)

    def test_course_enrollment(self):
        """Test student enrollment endpoint"""
        self.client.force_authenticate(user=self.admin)
        url = reverse('course-enroll-student', kwargs={'pk': self.course.pk})
        
        data = {'student_id': self.student.id}
        response = self.client.post(url, data)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(self.student, self.course.students.all())

    def test_course_enrollment_duplicate(self):
        """Test duplicate enrollment prevention"""
        self.course.students.add(self.student)
        
        self.client.force_authenticate(user=self.admin)
        url = reverse('course-enroll-student', kwargs={'pk': self.course.pk})
        
        data = {'student_id': self.student.id}
        response = self.client.post(url, data)
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_course_unenrollment(self):
        """Test student unenrollment endpoint"""
        self.course.students.add(self.student)
        
        self.client.force_authenticate(user=self.admin)
        url = reverse('course-unenroll-student', kwargs={'pk': self.course.pk})
        
        data = {'student_id': self.student.id}
        response = self.client.post(url, data)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotIn(self.student, self.course.students.all())

    def test_course_statistics(self):
        """Test course statistics endpoint"""
        self.client.force_authenticate(user=self.admin)
        url = reverse('course-statistics')
        
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        data = response.json()
        self.assertIn('total_courses', data)
        self.assertIn('active_courses', data)
        self.assertEqual(data['total_courses'], 1)

    def test_course_filtering(self):
        """Test course filtering"""
        self.client.force_authenticate(user=self.admin)
        url = reverse('course-list')
        
        # Test title filter
        response = self.client.get(url, {'title': 'Test'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, 'Test Course')
        
        # Test code filter
        response = self.client.get(url, {'code': 'TC101'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, 'TC101')

    def test_course_search(self):
        """Test course search functionality"""
        self.client.force_authenticate(user=self.admin)
        url = reverse('course-list')
        
        response = self.client.get(url, {'search': 'Test'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, 'Test Course')

    def test_course_ordering(self):
        """Test course ordering"""
        # Create another course
        Course.objects.create(
            title='Another Course',
            code='AC101',
            professor=self.professor
        )
        
        self.client.force_authenticate(user=self.admin)
        url = reverse('course-list')
        
        # Test ordering by title
        response = self.client.get(url, {'ordering': 'title'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        data = response.json()
        titles = [course['title'] for course in data['results']]
        self.assertEqual(titles, sorted(titles))

    def test_professor_course_access(self):
        """Test professor can only see their own courses"""
        # Create another professor and course
        other_professor = User.objects.create_user(
            username='other_prof',
            national_id='1234567893',
            email='other@test.com',
            password='testpass123',
            user_type='EMPLOYEE'
        )
        
        other_course = Course.objects.create(
            title='Other Course',
            code='OC101',
            professor=other_professor
        )
        
        self.client.force_authenticate(user=self.professor)
        url = reverse('course-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        
        # Professor should only see their own course
        self.assertEqual(len(data['results']), 1)
        self.assertEqual(data['results'][0]['title'], 'Test Course')

    def test_student_course_access(self):
        """Test student can only see enrolled courses"""
        self.course.students.add(self.student)
        
        self.client.force_authenticate(user=self.student)
        url = reverse('course-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        
        # Student should see enrolled courses
        self.assertEqual(len(data['results']), 1)
        self.assertEqual(data['results'][0]['title'], 'Test Course')


class CourseValidationTest(APITestCase):
    """Test Course validation"""

    def setUp(self):
        self.client = APIClient()
        self.admin = User.objects.create_user(
            username='admin',
            national_id='1234567890',
            email='admin@test.com',
            password='testpass123',
            user_type='ADMIN'
        )
        
        self.professor = User.objects.create_user(
            username='professor',
            national_id='1234567891',
            email='prof@test.com',
            password='testpass123',
            user_type='EMPLOYEE'
        )

    def test_course_title_validation(self):
        """Test course title validation"""
        self.client.force_authenticate(user=self.admin)
        url = reverse('course-list')
        
        # Test empty title
        data = {
            'title': '',
            'code': 'TC101',
            'professor': self.professor.id
        }
        
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_course_code_uniqueness(self):
        """Test course code uniqueness"""
        Course.objects.create(
            title='Existing Course',
            code='TC101',
            professor=self.professor
        )
        
        self.client.force_authenticate(user=self.admin)
        url = reverse('course-list')
        
        data = {
            'title': 'New Course',
            'code': 'TC101',  # Duplicate code
            'professor': self.professor.id
        }
        
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('code', response.json())

    def test_professor_validation(self):
        """Test professor validation"""
        student = User.objects.create_user(
            username='student',
            national_id='1234567892',
            email='student@test.com',
            password='testpass123',
            user_type='STUDENT'
        )
        
        self.client.force_authenticate(user=self.admin)
        url = reverse('course-list')
        
        data = {
            'title': 'Test Course',
            'code': 'TC101',
            'professor': student.id  # Student as professor
        }
        
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
