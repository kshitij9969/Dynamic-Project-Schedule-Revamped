from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework.test import APIClient
from rest_framework import status

from faker import Faker

from core import models
from core.test.test_model import get_sample_employee_id

import uuid

import json

LOGIN_URL = reverse('user:token')
LOGOUT_URL = reverse('user:logout')
HOME_PAGE_URL = reverse('user:homepage')
# CREATE_ORG_URL = reverse('user:create-org')
# CREATE_MANAGER_URL = reverse('user:create-manager')
# CREATE_ASSOCIATE_URL = reverse('user:create-associate')
UPDATE_ORGANISATION_URL = reverse('user:update-org')
UPDATE_MANAGER_URL = reverse('user:update-manager')
UPDATE_ASSOCIATE_URL = reverse('user:update-associate')
FETCH_ASSOCIATES_LIST_URL = reverse('user:get-associate-list')
FETCH_MANAGERS_LIST_URL = reverse('user:get-manager-list')
DELETE_ORG_URL = reverse('user:delete-org')
DELETE_MANAGER_URL = reverse('user:delete-manager')
DELETE_ASSOCIATE_URL = reverse('user:delete-associate')
GET_MY_PROFILE_URL = reverse('user:get-my-profile')
CHANGE_PASSWORD_URL = reverse('user:change-password')

fake = Faker()


def sample_user_payload():
    """
    Returns a sample user payload
    :return: Dictionary object
    """
    return {
        'username': str(uuid.uuid4()),
        'full_name': fake.name(),
        'nick_name': fake.name(),
        'email': fake.company_email(),
        'password': 'test123$$$',
    }


def sample_org_payload():
    """
    Returns a sample organisation payload
    :return: Dictionary object
    """
    return {**{
        'username': str(uuid.uuid4()),
        'full_name': fake.name(),
        'nick_name': fake.name(),
        'email': fake.company_email(),
        'password': 'test123$$$',
    }, **{
        'industry': 'IT',
        'country_code': fake.country_calling_code(),
        'contact_no': fake.phone_number(),
        'address_line_one': fake.street_name(),
        'address_line_two': fake.street_name(),
        'country': fake.country(),
        'province_state': 'Maharashtra',
        'city': fake.city()
    }}


def sample_organisation_only_payload():
    """
    Returns organisation only payload(without user details)
    :return: Dictionary object
    """
    return {
            'industry': 'IT',
            'country_code': fake.country_calling_code(),
            'contact_no': fake.phone_number(),
            'address_line_one': fake.street_name(),
            'address_line_two': fake.street_name(),
            'country': fake.country(),
            'province_state': 'Maharashtra',
            'city': fake.city()
        }


def sample_manager_payload():
    """
    Returns manager payload
    :return: Dictionary object
    """
    return {
        'user_account': {
            'username': uuid.uuid4(),
            'full_name': fake.name(),
            'nick_name': fake.name(),
            'email': fake.company_email(),
            'password': 'test123$$$'
        },
        **{'employee_id': get_sample_employee_id(), }
            }


def sample_associate_payload():
    """
    Returns associate payload
    :return: Dictionary object
    """
    return {
        'user_account': {
            'username': uuid.uuid4(),
            'full_name': fake.name(),
            'nick_name': fake.name(),
            'email': fake.company_email(),
            'password': 'test123$$$'
                       },
        **{'employee_id': get_sample_employee_id(),}
            }


def create_user(**params):
    """
    Helper function to create user
    :param params: parameters to create User object
    :return: User object
    """
    return get_user_model().objects.create_user(**params)


def create_organisation(**params):
    """
    Helper function to create OrganisationAccount object
    :param params: parameters to create OrganisationAccount object
    :return: OrganisationAccount object
    """
    return models.OrganisationAccount.objects.\
        create_org_account(**params)


def create_manager(**params):
    """
    Helper function to create ManagerAccount object
    :param params: parameters to create ManagerAccount object
    :return: ManagerAccount object
    """
    return models.ManagerAccount.objects.create_manager_account(**params)


def create_associate(**params):
    """
    Helper function to create AssociateAccount object
    :param params: parameters to create AssociateAccount object
    :return: AssociateAccount object
    """
    return models.AssociateAccount.objects.create_associate_account(**params)


class PublicApiTest(TestCase):
    """
    Class to test all public APIs
    """

    def test_login_is_successful(self):
        """
        Test that a user is able to login successfully
        :return: None
        """
        pass

    def test_create_organisation_account_is_successful(self):
        """
        Test that an OrganisationAccount can be created successfully
        :return: None
        """
        pass


class HomePageApiTest(TestCase):
    """
    Class to test all private APIs(the ones that require login)
    """

    def setUp(self) -> None:
        """
        Setup for the following tests
        :return: None
        """
        self.api_client = APIClient()
        self.user = create_user(**sample_user_payload())
        self.org = create_organisation(user_account=self.user, **sample_organisation_only_payload())
        self.user.refresh_from_db()

        # user accounts for manager and associates
        self.manager_one_user = create_user(**sample_user_payload())
        self.manager_two_user = create_user(**sample_user_payload())
        self.manager_three_user = create_user(**sample_user_payload())

        self.associate_one_user = create_user(**sample_user_payload())
        self.associate_two_user = create_user(**sample_user_payload())
        self.associate_three_user = create_user(**sample_user_payload())
        self.associate_four_user = create_user(**sample_user_payload())
        self.associate_five_user = create_user(**sample_user_payload())
        self.associate_six_user = create_user(**sample_user_payload())

        # Add some manager in the organisation
        self.manager_one = create_manager(user_account=self.manager_one_user,
                                     belongs_to=self.org,
                                     employee_id=get_sample_employee_id())
        self.manager_one_user.refresh_from_db()

        self.manager_two = create_manager(user_account=self.manager_two_user,
                                     belongs_to=self.org,
                                     employee_id=get_sample_employee_id())
        self.manager_two_user.refresh_from_db()

        self.manager_three = create_manager(user_account=self.manager_three_user,
                                       belongs_to=self.org,
                                       employee_id=get_sample_employee_id())
        self.manager_three_user.refresh_from_db()

        # Add some associates under manager
        self.associate_one = create_associate(user_account=self.associate_one_user,
                                         belongs_to=self.org,
                                         employee_id=get_sample_employee_id(),
                                         reports_to=self.manager_one
                                         )
        self.associate_one_user.refresh_from_db()

        self.associate_two = create_associate(user_account=self.associate_two_user,
                                         belongs_to=self.org,
                                         employee_id=get_sample_employee_id(),
                                         reports_to=self.manager_one
                                         )
        self.associate_two_user.refresh_from_db()

        self.associate_three = create_associate(user_account=self.associate_three_user,
                                           belongs_to=self.org,
                                           employee_id=get_sample_employee_id(),
                                           reports_to=self.manager_one
                                           )
        self.associate_three_user.refresh_from_db()

        self.associate_four = create_associate(user_account=self.associate_four_user,
                                          belongs_to=self.org,
                                          employee_id=get_sample_employee_id(),
                                          reports_to=self.manager_two
                                          )
        self.associate_four_user.refresh_from_db()

        self.associate_five = create_associate(user_account=self.associate_five_user,
                                          belongs_to=self.org,
                                          employee_id=get_sample_employee_id(),
                                          reports_to=self.manager_two
                                          )
        self.associate_five_user.refresh_from_db()

        self.associate_six = create_associate(user_account=self.associate_six_user,
                                         belongs_to=self.org,
                                         employee_id=get_sample_employee_id(),
                                         reports_to=self.manager_three
                                         )
        self.associate_six_user.refresh_from_db()

        self.api_client.credentials()

    def test_home_page_for_organisation_account(self):
        """
        Test the home page for organisation account
        :return: None
        """
        TOKEN_PAYLOAD = {
            'username': self.user.username,
            'password': 'test123$$$',
            'device-identifier': str(uuid.uuid4())
        }

        res = self.api_client.post(LOGIN_URL, TOKEN_PAYLOAD)
        self.api_client.credentials(HTTP_AUTHORIZATION='Token ' + res.data.get('token'))

        res = self.api_client.get(HOME_PAGE_URL)

        res = res.data
        self.assertEqual(self.user.username, res.get('username'))
        self.assertNotIn('password', res)

        self.assertEqual(self.manager_one_user.username,
                         res.get('managers')[0].get('username'))
        self.assertEqual(self.manager_two_user.username,
                         res.get('managers')[1].get('username'))
        self.assertEqual(self.manager_three_user.username,
                         res.get('managers')[2].get('username'))

        self.assertEqual(self.associate_one_user.username,
                         res.get('associates')[0].get('username'))
        self.assertEqual(self.associate_two_user.username,
                         res.get('associates')[1].get('username'))
        self.assertEqual(self.associate_three_user.username,
                         res.get('associates')[2].get('username'))
        self.assertEqual(self.associate_four_user.username,
                         res.get('associates')[3].get('username'))
        self.assertEqual(self.associate_five_user.username,
                         res.get('associates')[4].get('username'))
        self.assertEqual(self.associate_six_user.username,
                         res.get('associates')[5].get('username'))

    def test_home_page_for_manager_account(self):
        """
        Test the home page for manager account
        :return: None
        """
        TOKEN_PAYLOAD = {
            'username': self.manager_one_user.username,
            'password': 'test123$$$',
            'device-identifier': str(uuid.uuid4())
        }

        res = self.api_client.post(LOGIN_URL, TOKEN_PAYLOAD)
        self.api_client.credentials(HTTP_AUTHORIZATION='Token ' + res.data.get('token'))

        res = self.api_client.get(HOME_PAGE_URL)

        res = res.data

        self.assertEqual(self.manager_one_user.username,
                         res.get('username'))
        self.assertNotIn('password', res)

        self.assertEqual(self.user.username,
                         res.get('organisation')[0].get('username'))

        self.assertEqual(self.associate_one_user.username,
                         res.get('associates')[0].get('username'))
        self.assertEqual(self.associate_two_user.username,
                         res.get('associates')[1].get('username'))
        self.assertEqual(self.associate_three_user.username,
                         res.get('associates')[2].get('username'))

    def test_home_page_for_associate_account(self):
        """
        Test the home page for associate account
        :return: None
        """
        TOKEN_PAYLOAD = {
            'username': self.associate_one_user.username,
            'password': 'test123$$$',
            'device-identifier': str(uuid.uuid4())
        }

        res = self.api_client.post(LOGIN_URL, TOKEN_PAYLOAD)
        self.api_client.credentials(HTTP_AUTHORIZATION='Token ' + res.data.get('token'))

        res = self.api_client.get(HOME_PAGE_URL)

        res = res.data

        self.assertEqual(self.associate_one_user.username,
                         res.get('username'))
        self.assertNotIn('password', res)
        self.assertEqual(self.user.username,
                         res.get('organisation')[0].get('username'))
        self.assertEqual(self.manager_one_user.username,
                         res.get('manager')[0].get('username'))

    def test_update_organisation_account_is_successful(self):
        """
        Test that organisation account update is successful
        :return: None
        """
        TOKEN_PAYLOAD = {
            'username': self.user.username,
            'password': 'test123$$$',
            'device-identifier': str(uuid.uuid4())
        }

        res = self.api_client.post(LOGIN_URL, TOKEN_PAYLOAD)
        self.api_client.credentials(HTTP_AUTHORIZATION='Token ' + res.data.get('token'))

        update_org_payload = {
            'user_account':{
                # 'username': str(uuid.uuid4()),
                'full_name': 'new_full_name',
                'nick_name': 'new_nick_name',
                'email': 'test@test.com',
                # 'password': 'test123$$$',
            },
            'industry': 'Manufacturing',
            'country_code': '91',
            'contact_no': '1234567789',
            'address_line_one': 'fake address',
            'address_line_two': 'fake address',
            'address_line_three': 'fake address',
            'country': 'India',
            'province_state': 'Maharashtra',
            'city': 'Mumbai'
        }

        res = self.api_client.patch(UPDATE_ORGANISATION_URL, update_org_payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(update_org_payload.get('user_account').get('full_name'),
                         res.data.get('user_account').get('full_name'))
        self.assertEqual(update_org_payload.get('user_account').get('nick_name'),
                         res.data.get('user_account').get('nick_name'))
        self.assertEqual(update_org_payload.get('user_account').get('email'),
                         res.data.get('user_account').get('email'))

        res.data.pop('user_account')
        res.data.pop('id')
        update_org_payload.pop('user_account')

        self.assertDictEqual(res.data, update_org_payload)

    def test_update_manager_account_is_successful(self):
        """
        Test that manager account update is successful
        :return: None
        """
        TOKEN_PAYLOAD = {
            'username': self.manager_one_user.username,
            'password': 'test123$$$',
            'device-identifier': str(uuid.uuid4())
        }

        res = self.api_client.post(LOGIN_URL, TOKEN_PAYLOAD)
        self.api_client.credentials(HTTP_AUTHORIZATION='Token ' + res.data.get('token'))

        update_manager_payload = {
            'user_account': {
                # 'username': str(uuid.uuid4()),
                'full_name': 'new_full_name',
                'nick_name': 'new_nick_name',
                'email': 'test@test.com',
                # 'password': 'test123$$$',
            },
            'employee_id': get_sample_employee_id()
        }

        res = self.api_client.patch(UPDATE_MANAGER_URL, update_manager_payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(update_manager_payload.get('user_account').get('full_name'),
                         res.data.get('user_account').get('full_name'))
        self.assertEqual(update_manager_payload.get('user_account').get('nick_name'),
                         res.data.get('user_account').get('nick_name'))
        self.assertEqual(update_manager_payload.get('user_account').get('email'),
                         res.data.get('user_account').get('email'))

        self.assertEqual(str(update_manager_payload.get('employee_id')),
                         res.data.get('employee_id'))

    def test_update_associate_account_is_successful(self):
        """
        Test that associate account update is successful
        :return: None
        """
        TOKEN_PAYLOAD = {
            'username': self.associate_one_user.username,
            'password': 'test123$$$',
            'device-identifier': str(uuid.uuid4())
        }

        res = self.api_client.post(LOGIN_URL, TOKEN_PAYLOAD)
        self.api_client.credentials(HTTP_AUTHORIZATION='Token ' + res.data.get('token'))

        update_associate_payload = {
            'user_account': {
                # 'username': str(uuid.uuid4()),
                'full_name': 'new_full_name',
                'nick_name': 'new_nick_name',
                'email': 'test@test.com',
                # 'password': 'test123$$$',
            },
            'employee_id': get_sample_employee_id()
        }

        res = self.api_client.patch(UPDATE_ASSOCIATE_URL, update_associate_payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(update_associate_payload.get('user_account').get('full_name'),
                         res.data.get('user_account').get('full_name'))
        self.assertEqual(update_associate_payload.get('user_account').get('nick_name'),
                         res.data.get('user_account').get('nick_name'))
        self.assertEqual(update_associate_payload.get('user_account').get('email'),
                         res.data.get('user_account').get('email'))

        self.assertEqual(str(update_associate_payload.get('employee_id')),
                         res.data.get('employee_id'))

    def test_fetch_list_of_manager_is_successful(self):
        """
        Test fetch list of managers is successful
        :return: None
        """
        TOKEN_PAYLOAD = {
            'username': self.user.username,
            'password': 'test123$$$',
            'device-identifier': str(uuid.uuid4())
        }

        res = self.api_client.post(LOGIN_URL, TOKEN_PAYLOAD)
        self.api_client.credentials(HTTP_AUTHORIZATION='Token ' + res.data.get('token'))

        res = self.api_client.get(FETCH_MANAGERS_LIST_URL)

        self.assertEqual(self.manager_one_user.username,
                         res.data.get('managers')[0].get('username'))
        self.assertEqual(self.manager_two_user.username,
                         res.data.get('managers')[1].get('username'))
        self.assertEqual(self.manager_three_user.username,
                         res.data.get('managers')[2].get('username'))

    def test_fetch_list_of_associate_is_successful(self):
        """
        Test fetch list of associates is successful
        :return: None
        """
        TOKEN_PAYLOAD = {
            'username': self.user.username,
            'password': 'test123$$$',
            'device-identifier': str(uuid.uuid4())
        }

        res = self.api_client.post(LOGIN_URL, TOKEN_PAYLOAD)
        self.api_client.credentials(HTTP_AUTHORIZATION='Token ' + res.data.get('token'))

        res = self.api_client.get(FETCH_ASSOCIATES_LIST_URL)

        self.assertEqual(self.associate_one_user.username,
                         res.data.get('associates')[0].get('username'))
        self.assertEqual(self.associate_two_user.username,
                         res.data.get('associates')[1].get('username'))
        self.assertEqual(self.associate_three_user.username,
                         res.data.get('associates')[2].get('username'))
        self.assertEqual(self.associate_four_user.username,
                         res.data.get('associates')[3].get('username'))
        self.assertEqual(self.associate_five_user.username,
                         res.data.get('associates')[4].get('username'))
        self.assertEqual(self.associate_six_user.username,
                         res.data.get('associates')[5].get('username'))

        TOKEN_PAYLOAD = {
            'username': self.manager_one_user.username,
            'password': 'test123$$$',
            'device-identifier': str(uuid.uuid4())
        }

        res = self.api_client.post(LOGIN_URL, TOKEN_PAYLOAD)
        self.api_client.credentials(HTTP_AUTHORIZATION='Token ' + res.data.get('token'))

        res = self.api_client.get(FETCH_ASSOCIATES_LIST_URL)

        self.assertEqual(self.associate_one_user.username,
                         res.data.get('associates')[0].get('username'))
        self.assertEqual(self.associate_two_user.username,
                         res.data.get('associates')[1].get('username'))
        self.assertEqual(self.associate_three_user.username,
                         res.data.get('associates')[2].get('username'))

    def test_organisation_delete_is_successful(self):
        """
        Test that organisation account deletion is successful
        :return: None
        """
        TOKEN_PAYLOAD = {
            'username': self.user.username,
            'password': 'test123$$$',
            'device-identifier': str(uuid.uuid4())
        }

        res = self.api_client.post(LOGIN_URL, TOKEN_PAYLOAD)
        self.api_client.credentials(HTTP_AUTHORIZATION='Token ' + res.data.get('token'))

        res = self.api_client.delete(DELETE_ORG_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertFalse(models.User.objects.filter(username=self.user.username).exists())

        self.assertFalse(models.User.objects.filter(username=self.manager_one_user.username).exists())
        self.assertFalse(models.User.objects.filter(username=self.manager_two_user.username).exists())
        self.assertFalse(models.User.objects.filter(username=self.manager_three_user.username).exists())

        self.assertFalse(models.User.objects.filter(username=self.associate_one_user.username).exists())
        self.assertFalse(models.User.objects.filter(username=self.associate_two_user.username).exists())
        self.assertFalse(models.User.objects.filter(username=self.associate_three_user.username).exists())
        self.assertFalse(models.User.objects.filter(username=self.associate_four_user.username).exists())
        self.assertFalse(models.User.objects.filter(username=self.associate_five_user.username).exists())
        self.assertFalse(models.User.objects.filter(username=self.associate_six_user.username).exists())

    def test_manager_delete_is_successful(self):
        """
        Test that ManagerAccount deletion is successful
        :return: None
        """
        TOKEN_PAYLOAD = {
            'username': self.user.username,
            'password': 'test123$$$',
            'device-identifier': str(uuid.uuid4())
        }

        res = self.api_client.post(LOGIN_URL, TOKEN_PAYLOAD)
        self.api_client.credentials(HTTP_AUTHORIZATION='Token ' + res.data.get('token'))

        payload = {
            'username': self.manager_one_user.username
        }
        res = self.api_client.delete(DELETE_MANAGER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertTrue(models.User.objects.filter(username=self.user.username).exists())

        self.assertFalse(models.User.objects.filter(username=self.manager_one_user.username).exists())
        self.assertTrue(models.User.objects.filter(username=self.manager_two_user.username).exists())
        self.assertTrue(models.User.objects.filter(username=self.manager_three_user.username).exists())

        self.assertFalse(models.User.objects.filter(username=self.associate_one_user.username).exists())
        self.assertFalse(models.User.objects.filter(username=self.associate_two_user.username).exists())
        self.assertFalse(models.User.objects.filter(username=self.associate_three_user.username).exists())
        self.assertTrue(models.User.objects.filter(username=self.associate_four_user.username).exists())
        self.assertTrue(models.User.objects.filter(username=self.associate_five_user.username).exists())
        self.assertTrue(models.User.objects.filter(username=self.associate_six_user.username).exists())

    def test_delete_associate_is_successful(self):
        """
        Test that AssociateAccount deletion is successful
        :return: None
        """
        TOKEN_PAYLOAD = {
            'username': self.manager_one_user.username,
            'password': 'test123$$$',
            'device-identifier': str(uuid.uuid4())
        }

        res = self.api_client.post(LOGIN_URL, TOKEN_PAYLOAD)
        self.api_client.credentials(HTTP_AUTHORIZATION='Token ' + res.data.get('token'))

        payload = {
            'username': self.associate_one_user.username
        }
        res = self.api_client.delete(DELETE_ASSOCIATE_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertTrue(models.User.objects.filter(username=self.user.username).exists())

        self.assertTrue(models.User.objects.filter(username=self.manager_one_user.username).exists())
        self.assertTrue(models.User.objects.filter(username=self.manager_two_user.username).exists())
        self.assertTrue(models.User.objects.filter(username=self.manager_three_user.username).exists())

        self.assertFalse(models.User.objects.filter(username=self.associate_one_user.username).exists())
        self.assertTrue(models.User.objects.filter(username=self.associate_two_user.username).exists())
        self.assertTrue(models.User.objects.filter(username=self.associate_three_user.username).exists())
        self.assertTrue(models.User.objects.filter(username=self.associate_four_user.username).exists())
        self.assertTrue(models.User.objects.filter(username=self.associate_five_user.username).exists())
        self.assertTrue(models.User.objects.filter(username=self.associate_six_user.username).exists())

    def test_get_my_profile_is_successful(self):
        """
        Test that fetch profile is successful
        :return: None
        """
        TOKEN_PAYLOAD = {
            'username': self.user.username,
            'password': 'test123$$$',
            'device-identifier': str(uuid.uuid4())
        }

        res = self.api_client.post(LOGIN_URL, TOKEN_PAYLOAD)
        self.api_client.credentials(HTTP_AUTHORIZATION='Token ' + res.data.get('token'))

        res = self.api_client.get(GET_MY_PROFILE_URL)
        self.assertEqual(str(self.user.username), res.data.get('username'))

        TOKEN_PAYLOAD = {
            'username': self.manager_one_user.username,
            'password': 'test123$$$',
            'device-identifier': str(uuid.uuid4())
        }

        res = self.api_client.post(LOGIN_URL, TOKEN_PAYLOAD)
        self.api_client.credentials(HTTP_AUTHORIZATION='Token ' + res.data.get('token'))

        res = self.api_client.get(GET_MY_PROFILE_URL)
        self.assertEqual(self.manager_one_user.username, res.data.get('username'))

        TOKEN_PAYLOAD = {
            'username': self.associate_one_user.username,
            'password': 'test123$$$',
            'device-identifier': str(uuid.uuid4())
        }

        res = self.api_client.post(LOGIN_URL, TOKEN_PAYLOAD)
        self.api_client.credentials(HTTP_AUTHORIZATION='Token ' + res.data.get('token'))

        res = self.api_client.get(GET_MY_PROFILE_URL)
        self.assertEqual(self.associate_one_user.username, res.data.get('username'))

    def test_reset_password_is_successful(self):
        """
        Test that password reset is successful
        :return: None
        """
        TOKEN_PAYLOAD = {
            'username': self.user.username,
            'password': 'test123$$$',
            'device-identifier': str(uuid.uuid4())
        }

        res = self.api_client.post(LOGIN_URL, TOKEN_PAYLOAD)
        self.api_client.credentials(HTTP_AUTHORIZATION='Token ' + res.data.get('token'))

        change_password_payload = {
            'current_password': 'test123$$$',
            'new_password': 'newpassword123$$$'
        }

        res = self.api_client.post(CHANGE_PASSWORD_URL, change_password_payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

        TOKEN_PAYLOAD = {
            'username': self.user.username,
            'password': 'newpassword123$$$',
            'device-identifier': str(uuid.uuid4())
        }
        self.api_client.credentials()
        res = self.api_client.post(LOGIN_URL, TOKEN_PAYLOAD)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn('token', res.data)








