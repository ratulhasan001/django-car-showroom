from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class AuthFlowTests(TestCase):
    def test_register_then_login_and_logout(self):
        response = self.client.post(reverse('register'), {
            'username': 'newuser',
            'first_name': 'New',
            'last_name': 'User',
            'email': 'new@example.com',
            'password1': 'a-strong-pass-123',
            'password2': 'a-strong-pass-123',
        })
        self.assertRedirects(response, reverse('user_login'))
        self.assertTrue(User.objects.filter(username='newuser', email='new@example.com').exists())

        response = self.client.post(reverse('user_login'), {'username': 'newuser', 'password': 'a-strong-pass-123'})
        self.assertRedirects(response, reverse('homepage'))

        # Logging out needs a POST request.
        self.assertEqual(self.client.get(reverse('user_logout')).status_code, 405)
        response = self.client.post(reverse('user_logout'))
        self.assertRedirects(response, reverse('user_login'))
        self.assertNotIn('_auth_user_id', self.client.session)

    def test_registration_errors_are_shown(self):
        response = self.client.post(reverse('register'), {'username': 'x', 'password1': 'a', 'password2': 'b'})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['form'].errors)

    def test_wrong_password_shows_message(self):
        User.objects.create_user('sam', password='pass12345!')
        response = self.client.post(reverse('user_login'), {'username': 'sam', 'password': 'wrong'})
        self.assertContains(response, 'Login information is incorrect')

    def test_login_honours_next(self):
        User.objects.create_user('sam', password='pass12345!')
        response = self.client.post(
            reverse('user_login') + '?next=' + reverse('profile'),
            {'username': 'sam', 'password': 'pass12345!'},
        )
        self.assertRedirects(response, reverse('profile'))

    def test_profile_pages_require_login(self):
        for name in ['profile', 'edit_profile', 'pass_change']:
            with self.subTest(name=name):
                url = reverse(name)
                self.assertRedirects(self.client.get(url), f"{reverse('user_login')}?next={url}")

    def test_edit_profile_and_change_password(self):
        user = User.objects.create_user('sam', password='pass12345!')
        self.client.force_login(user)
        response = self.client.post(reverse('edit_profile'), {
            'username': 'sam', 'first_name': 'Samuel', 'last_name': 'Lee', 'email': 'sam@example.com',
        })
        self.assertRedirects(response, reverse('profile'))
        user.refresh_from_db()
        self.assertEqual(user.first_name, 'Samuel')

        response = self.client.post(reverse('pass_change'), {
            'old_password': 'pass12345!',
            'new_password1': 'another-pass-456',
            'new_password2': 'another-pass-456',
        })
        self.assertRedirects(response, reverse('profile'))
        user.refresh_from_db()
        self.assertTrue(user.check_password('another-pass-456'))
