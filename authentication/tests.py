from django.test import TestCase
from ninja.testing import TestClient, TestAsyncClient
from authentication.views import router
from authentication.models import User
from asgiref.sync import sync_to_async


class RegisterUserTest(TestCase):
    def test_without_payload(self):
        client = TestClient(router)
        response = client.post(path="/register")
        self.assertEqual(response.status_code, 422)

    def test_with_payload(self):
        client = TestClient(router)
        response = client.post(
            path="/register",
            json={"email": "test@mail.com", "password": "password"},
        )

        self.assertEqual(response.status_code, 200)


class LoginUserTest(TestCase):
    async def test_without_payload(self):
        client = TestAsyncClient(router)
        response = await client.post(path="/login")

        self.assertEqual(response.status_code, 422)

    async def test_with_payload(self):
        client = TestAsyncClient(router)
        response = await client.post(
            path="/login",
            json={"email": "test@mail.com", "password": "password"},
        )

        self.assertEqual(response.status_code, 401)
