from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User


class LoginPageTests(TestCase):
    def test_get_login_renders_page_and_registration_link(self):
        response = self.client.get(reverse("login"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "registration/login.html")
        self.assertContains(response, reverse("registrar"))


class CreateUserRedirectTests(TestCase):
    def test_redirects_to_home_after_registration(self):
        response = self.client.post(
            reverse("users"),
            {
                "username": "newuser",
                "email": "newuser@example.com",
                "password": "test-password-123",
            },
        )

        self.assertRedirects(response, reverse("movie_list"))
        self.assertTrue(User.objects.filter(username="newuser").exists())

    def test_shows_error_when_username_already_exists(self):
        User.objects.create_user(
            username="existinguser",
            email="existing@example.com",
            password="test-password-123",
        )

        response = self.client.post(
            reverse("users"),
            {
                "username": "existinguser",
                "email": "another@example.com",
                "password": "another-password-123",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Esse nome de usuário já está em uso.")
        self.assertEqual(User.objects.filter(username="existinguser").count(), 1)
