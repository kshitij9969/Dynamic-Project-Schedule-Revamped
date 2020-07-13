from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

import uuid

from faker import Faker

CREATE_USER_URL = reverse('user:create')
# TOKEN_URL = reverse('user:token')
# ME_URL = reverse('user:me')

fake = Faker()

SAMPLE_USER_PAYLOAD = {
    'username': uuid.uuid4(),
    'full_name': fake.name(),
    'nick_name': fake.name(),
    'email': fake.company_email(),
    'password': uuid.uuid4(),
}


def create_user(**params):
    """
    Helper function to create user
    :param params: parameters to create user object
    :return: User object
    """
    return get_user_model().objects.create_user(**params)


class PublicUserApiTest(TestCase):
    """
    Test the public APIs for User app
    """
    def setUp(self) -> None:
        """
        Setup for the test
        :return: None
        """
        self.api_client = APIClient()

    def test_create_user_valid_credentials(self):
        """
        Test that User object can be created using the API
        :return: None
        """
        res = self.api_client.post(CREATE_USER_URL, SAMPLE_USER_PAYLOAD)
        user = get_user_model().objects.get(**res.data)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertTrue(user.check_password(SAMPLE_USER_PAYLOAD['password']))
        self.assertNotIn('password', res.data)

    def test_user_exists(self):
        """
        Test that multiple user accounts cannot be created with same credentials
        :return: None
        """
        create_user(**SAMPLE_USER_PAYLOAD)

        res = self.api_client.post(CREATE_USER_URL, SAMPLE_USER_PAYLOAD)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

