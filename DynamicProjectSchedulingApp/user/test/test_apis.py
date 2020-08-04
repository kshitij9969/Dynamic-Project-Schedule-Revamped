from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework.test import APIClient

from faker import Faker

from core import models
from core.test.test_model import get_sample_employee_id

import uuid

LOGIN_URL = reverse('user:token')
LOGOUT_URL = reverse('user:logout')
HOME_PAGE_URL = reverse('user:homepage')
# CREATE_ORG_URL = reverse('user:create-org')
# CREATE_MANAGER_URL = reverse('user:create-manager')
# CREATE_ASSOCIATE_URL = reverse('user:create-associate')

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
        print(res.data)

    def test_home_page_for_manager_account(self):
        """
        Test the home page for manager account
        :return: None
        """
        pass

    def test_home_page_for_associate_account(self):
        """
        Test the home page for associate account
        :return: None
        """
        pass
