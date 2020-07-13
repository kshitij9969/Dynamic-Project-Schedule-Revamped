from django.test import TestCase
from django.contrib.auth import get_user_model
from django.db import IntegrityError

from core import models

from faker import Faker

import uuid, random

"""
Helper functions and identifiers to get sample objects needed for testing
"""

fake = Faker()


def get_sample_employee_id():
    """
    Generates a sample employee_id
    :return: integer
    """
    return random.randint(1000000000, 9999999999)


def sample_user(email=fake.company_email(), password=uuid.uuid4(),
                full_name=fake.name(), nick_name=fake.name()):
    """
    Creates a sample user for testing
    :param email: Email of user
    :param password: password of user
    :param full_name: first name of user
    :param nick_name: last name of user
    :return: User object
    """
    return get_user_model().objects.create_user(username=uuid.uuid4(),email=email, password=password,
                                                full_name=full_name, nick_name=nick_name
                                                )


def sample_organisation(industry='IT', country_code=fake.country_calling_code(),
                        contact_no=fake.phone_number(), address_line_one=fake.street_name(),
                        address_line_two=fake.street_name(), country=fake.country(), province_state='Maharashtra',
                        city=fake.city()):
    """
    Creates a sample organisation account for testing
    :param industry: Industry
    :param country_code: Country code
    :param contact_no: Contact number
    :param address_line_one: Address
    :param address_line_two: Address
    :param country: Country
    :param province_state: State
    :param city: City
    :return: OrganisationAccount object
    """
    user_account = sample_user(email=fake.company_email())
    return models.OrganisationAccount.objects.create_org_account(
                                      user_account=user_account,
                                      industry=industry,
                                      country_code=country_code, contact_no=contact_no,
                                      address_line_one=address_line_one,
                                      address_line_two=address_line_two, country=country,
                                      province_state=province_state, city=city)


def sample_manager(employee_id=get_sample_employee_id()):
    """
    Creates a sample manager account for testing
    :param user_account: User model object
    :param belongs_to: OrganisationAccount object
    :param employee_id: employee_id of manager
    :return: ManagerAccount object
    """
    email = fake.company_email()
    belongs_to = sample_organisation()
    return models.ManagerAccount.objects.create_manager_account(
                                user_account=sample_user(email=email),
                                belongs_to=belongs_to,
                                employee_id=employee_id)


def sample_associate(employee_id=get_sample_employee_id()):
    """
    Creates a sample associate account for testing
    :param user_account: User model object
    :param belongs_to: OrganisationAccount object
    :param employee_id: employee_id of associate
    :return: AssociateAccount object
    """
    email = fake.company_email()
    belongs_to = sample_organisation()
    return models.AssociateAccount.objects.create_associate_account(
                                   user_account=sample_user(email=email),
                                   belongs_to=belongs_to,
                                   employee_id=employee_id)


class UserModelTest(TestCase):
    """
    Class for testing User model
    """
    """
    Function to test creating a user with all details right
    """
    def test_create_user_with_all_detail_is_successful(self):
        """
        Test creating user object with all details is successful
        :return: None
        """

        email = fake.company_email()
        password = uuid.uuid4()
        full_name = fake.name()
        nick_name = fake.name()
        user = get_user_model().objects.create_user(username=uuid.uuid4(),
            email=email, password=password, full_name=full_name,
            nick_name=nick_name)

        self.assertEqual(email, user.email)
        self.assertEqual(full_name, user.full_name)
        self.assertEqual(nick_name, user.nick_name)
        self.assertTrue(user.check_password(password), password)
        self.assertTrue(user.is_active)

    """
    Test creating a new user using invalid details(first_name, email etc.)
    """
    def test_new_user_email_is_normalized(self):
        """
        Test that the email of a new user is normalized
        :return: None
        """
        email = 'test@DOMAIN.COM'
        password = uuid.uuid4()
        full_name = fake.name()
        nick_name = fake.name()
        user = get_user_model().objects.create_user(
            username=uuid.uuid4(),
            email=email, password=password, full_name=full_name,
            nick_name=nick_name)

        self.assertEqual(email.lower(), user.email)

    def test_create_new_user_with_invalid_email_is_unsuccessful(self):
        """
        Test that user object is not created with an invalid email address
        :return: None
        """
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(
                username=uuid.uuid4(),
                email=None,
                password=uuid.uuid4(),
                full_name=fake.name(),
                nick_name=fake.name()
            )

    def test_create_new_user_with_invalid_first_name_is_unsuccessful(self):
        """
        Test that user object is not created with an invalid first name
        :return: None
        """
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(
                username=uuid.uuid4(),
                email=fake.company_email(),
                password=uuid.uuid4(),
                full_name=None,
                nick_name=fake.name()
            )


    """
    Test if a superuser is created with valid details
    """
    def test_create_new_super_user_is_successful(self):
        """
        Test that a new super user is created
        :return: None
        """
        email = fake.company_email()
        password = uuid.uuid4()
        full_name = fake.name()
        nick_name = fake.name()
        user = get_user_model().objects.create_superuser(
            username=uuid.uuid4(),
            email=email, password=password, full_name=full_name,
            nick_name=nick_name)

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_active)

    """
    Test that the image is renamed after upload
    """

    def test_profile_picture_rename_is_successful(self):
        """
        Test that the image is renamed successfully
        :return: None
        """
        user = sample_user()
        image_path = models.rename_profile_picture(user, 'test.jpg')
        expected_image_path = f"{user.full_name}_{user.nick_name}.jpg"
        self.assertEqual(image_path, expected_image_path)


class OrganisationModelTest(TestCase):
    """
    Class for testing OrganisationAccount class
    """

    def test_create_organisation_account_is_successful(self):
        """
        Test that an organisation account is created successfully
        :return: None
        """
        user_account = sample_user()
        industry = 'IT'
        country_code = fake.country_code()
        contact_no = fake.phone_number()
        address_line_one = fake.street_name()
        address_line_two = fake.street_name()
        address_line_three = None
        country = fake.country()
        province_state = 'Maharashtra'
        city = fake.city()

        org_acc = models.OrganisationAccount.objects.create_org_account(
            user_account=user_account,
            industry='IT',
            country_code=country_code, contact_no=contact_no,
            address_line_one=address_line_one,
            address_line_two=address_line_two,
            address_line_three=address_line_three,
            country=country,
            province_state=province_state, city=city
        )

        self.assertEqual(org_acc.user_account, user_account)
        self.assertEqual(org_acc.industry, industry)
        self.assertEqual(org_acc.country_code, country_code)
        self.assertEqual(org_acc.contact_no, contact_no)
        self.assertEqual(org_acc.address_line_one, address_line_one)
        self.assertEqual(org_acc.address_line_two, address_line_two)
        self.assertEqual(org_acc.address_line_three, address_line_three)
        self.assertEqual(org_acc.country, country)
        self.assertEqual(org_acc.province_state, province_state)
        self.assertEqual(org_acc.city, city)

    def test_new_org_account_without_user_account_is_unsuccessful(self):
        """
        Test that a new organisation account cannot be created
         without first creating a user account
        :return: None
        """
        with self.assertRaises(ValueError):
            user_account = None
            industry = 'IT'
            country_code = fake.country_code()
            contact_no = fake.phone_number()
            address_line_one = fake.street_name()
            address_line_two = fake.street_name()
            address_line_three = None
            country = fake.country()
            province_state = 'Maharashtra'
            city = fake.city()

            models.OrganisationAccount.objects.create_org_account(
                user_account=user_account,
                industry=industry,
                country_code=country_code, contact_no=contact_no,
                address_line_one=address_line_one,
                address_line_two=address_line_two,
                address_line_three=address_line_three,
                country=country,
                province_state=province_state, city=city
            )

    def test_multiple_org_account_with_same_user_account_is_unsuccessful(self):
        """
        Test that multiple organisation account cannot
        be created with the same user account
        :return: None
        """
        with self.assertRaises(IntegrityError):
            user_account = sample_user()
            industry = 'IT'
            country_code = fake.country_code()
            contact_no = fake.phone_number()
            address_line_one = fake.street_name()
            address_line_two = fake.street_name()
            address_line_three = None
            country = fake.country()
            province_state = 'Maharashtra'
            city = fake.city()

            models.OrganisationAccount.objects.create_org_account(
                user_account=user_account,
                industry=industry,
                country_code=country_code, contact_no=contact_no,
                address_line_one=address_line_one,
                address_line_two=address_line_two,
                address_line_three=address_line_three,
                country=country,
                province_state=province_state, city=city
            )

            models.OrganisationAccount.objects.create_org_account(
                user_account=user_account,
                industry=industry,
                country_code=country_code, contact_no=contact_no,
                address_line_one=address_line_one,
                address_line_two=address_line_two,
                address_line_three=address_line_three,
                country=country,
                province_state=province_state, city=city
            )


class ManagerAccountModelTest(TestCase):
    """
    Class for testing ManagerAccount model
    """
    def test_manager_account_creation_is_successful(self):
        """
        Test that the new manager account creation is successful
        :return: None
        """
        user_account = sample_user()
        employee_id = get_sample_employee_id()
        org_account = sample_organisation()
        manager_acc = models.ManagerAccount.objects.create_manager_account(
            user_account=user_account,
            employee_id=employee_id,
            belongs_to=org_account
        )

        self.assertEqual(manager_acc.user_account, user_account)
        self.assertEqual(manager_acc.employee_id, employee_id)
        self.assertEqual(manager_acc.belongs_to, org_account)

    def test_new_manager_account_without_user_account_is_unsuccessful(self):
        """
        Test that a new manager account cannot be created without user account
        :return: None
        """
        with self.assertRaises(ValueError):
            user_org_account = get_user_model().objects.create_user(
                username=uuid.uuid4(),
                email=fake.email(), password=uuid.uuid4(),
                full_name=fake.name(), nick_name=fake.name()
            )
            employee_id = get_sample_employee_id()
            org_account = models.OrganisationAccount.objects.create_org_account(
                user_account=user_org_account,
                industry='IT',
                country_code='+91', contact_no=fake.phone_number(),
                address_line_one=fake.street_name(),
                address_line_two=fake.street_name(), country=fake.country(),
                province_state='Maharashtra', city=fake.city()
            )
            models.ManagerAccount.objects.create_manager_account(
                user_account=None,
                employee_id=employee_id,
                belongs_to=org_account
            )

    def test_multiple_manager_account_with_same_user_account_is_unsuccessful(self):
        """
        Test that multiple manager account cannot be created with same user account
        :return:
        """
        with self.assertRaises(IntegrityError):
            user_account = sample_user()
            org_acc = sample_organisation()

            emp_id_one = get_sample_employee_id()
            models.ManagerAccount.objects.create_manager_account(
                user_account=user_account,
                belongs_to=org_acc,
                employee_id=emp_id_one
            )

            emp_id_two = get_sample_employee_id()
            models.ManagerAccount.objects.create_manager_account(
                user_account=user_account,
                belongs_to=org_acc,
                employee_id=emp_id_two
            )


class AssociateAccountModelTest(TestCase):
    """
    Class for testing AssociateAccount model
    """
    def test_associate_account_creation_is_successful(self):
        """
        Test that an associate account can be successfully created
        :return: None
        """
        user_account = sample_user()
        org_account = sample_organisation()
        manager_account = sample_manager()
        employee_id = get_sample_employee_id()

        assoc_account = models.AssociateAccount.objects.create_associate_account(
            user_account=user_account,
            belongs_to=org_account,
            reports_to=manager_account,
            employee_id=employee_id
        )

        self.assertEqual(assoc_account.user_account, user_account)
        self.assertEqual(assoc_account.belongs_to, org_account)
        self.assertEqual(assoc_account.reports_to, manager_account)

    def test_new_associate_account_without_user_account_is_unsuccessful(self):
        """
        Test that a new associate account without a user account is unsuccessful
        :return: None
        """
        with self.assertRaises(ValueError):
            org_account = sample_organisation()
            manager_account = sample_manager()
            employee_id = get_sample_employee_id()
            models.AssociateAccount.objects.create_associate_account(
                user_account=None,
                belongs_to=org_account,
                reports_to=manager_account,
                employee_id=employee_id
            )

    def test_new_associate_account_without_organisation_account_is_unsuccessful(self):
        """
        Test that a new associate account without an organisation is unsuccessful
        :return: None
        """
        with self.assertRaises(ValueError):
            user_account = sample_user()
            manager_account = sample_manager()
            employee_id = get_sample_employee_id()

            models.AssociateAccount.objects.create_associate_account(
                user_account=user_account,
                belongs_to=None,
                reports_to=manager_account,
                employee_id=employee_id
            )

    def test_new_associate_account_without_manager_account_is_unsuccessful(self):
        """
        Test that a new associate account without a manager account is unsuccessful
        :return: None
        """
        with self.assertRaises(ValueError):
            user_account = sample_user()
            org_account = sample_organisation()
            employee_id = get_sample_employee_id()

            models.AssociateAccount.objects.create_associate_account(
                user_account=user_account,
                belongs_to=org_account,
                reports_to=None,
                employee_id=employee_id
            )
