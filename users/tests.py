from django.test import TestCase, Client
from django.urls import reverse
from users.models import UserInfo

class UserTests(TestCase):
    def setUp(self):
        """ Set up a test user and client """
        self.client = Client()
        self.user = UserInfo.objects.create(user_name="testuser@outlook.com", pwd="123123")

    def test_register_user(self):
        """ Test user registration """
        response = self.client.post(reverse('register'), {
            'user_name': 'newuser@example.com',
            'pwd': 'newpassword'
        })
        self.assertEqual(response.status_code, 302)  # Expect redirect after successful registration
        self.assertTrue(UserInfo.objects.filter(user_name='newuser@example.com').exists())

    def test_check_existing_username(self):
        """ Test checking if a username already exists """
        response = self.client.get(reverse('checkUserName'), {'user_name': 'testuser@outlook.com'})
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {'flag': True})  # Expect flag=True since user exists

    def test_check_non_existing_username(self):
        """ Test checking if a username does not exist """
        response = self.client.get(reverse('checkUserName'), {'user_name': 'nonexistent@example.com'})
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {'flag': False})  # Expect flag=False since user does not exist

    def test_login_success(self):
        """ Test successful login """
        response = self.client.post(reverse('login'), {
            'user_name': 'testuser@outlook.com',
            'pwd': '123123'
        })
        self.assertEqual(response.status_code, 302)  # Expect redirect to user center
        self.assertEqual(self.client.session.get('user_id'), self.user.id)  # Check if session user_id is set

    def test_login_failure(self):
        """ Test login failure with incorrect password """
        response = self.client.post(reverse('login'), {
            'user_name': 'testuser@outlook.com',
            'pwd': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Invalid username or password")

    def test_logout(self):
        """ Test logout functionality """
        self.client.session['user_id'] = self.user.id
        response = self.client.post(reverse('logout'))
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {'del_flag': True})  # Expect JSON response with del_flag=True
        self.assertNotIn('user_id', self.client.session)  # Ensure session is cleared

    def test_user_center_access(self):
        """ Test accessing user center when logged in """
        session = self.client.session
        session['user_id'] = self.user.id
        session.save()

        response = self.client.get(reverse('center'))
        self.assertEqual(response.status_code, 200)

        self.assertContains(response, f"[{self.user.user_name}]")

    def test_user_center_redirect_when_not_logged_in(self):
        """ Test user center redirects to login when not logged in """
        response = self.client.get(reverse('center'), follow=True)  # Expect redirect to login page
        self.assertRedirects(response, reverse('login'))  # Ensure redirected to login page

