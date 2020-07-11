from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models

import uuid

"""
Helper functions to get sample objects needed for testing
"""


def sample_user(email='test@test.com', password=uuid.uuid4(),
                full_name='test', nick_name='test', dob='2000-01-20'):
    """
    Creates a sample user for testing
    :param email: Email of user
    :param password: password of user
    :param full_name: first name of user
    :param nick_name: last name of user
    :param dob: date of birth of user
    :return: User object
    """
    return get_user_model().objects.create_user(email=email, password=password,
                                                full_name=full_name, nick_name=nick_name,
                                                dob=dob)


def sample_organisation(industry='IT', country_code='+91',
                        contact_no='1234567890', address_line_one='address_line_one',
                        address_line_two='address_line_two', country='India', province_state='Maharashtra',
                        city='Mumbai'):
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
    :return: OrganizationAccount object
    """
    user_account = sample_user(email='test2@test.com')
    return models.OrganizationAccount(user_account=user_account, industry=industry,
                                      country_code=country_code, contact_no=contact_no,
                                      address_line_one=address_line_one,
                                      address_line_two=address_line_two, country=country,
                                      province_state=province_state, city=city)


def sample_manager(belongs_to=sample_organisation(), employee_id='1234567890'):
    """
    Creates a sample manager account for testing
    :param user_account: User model object
    :param belongs_to: OrganisationAccount object
    :param employee_id: employee_id of manager
    :return: ManagerAccount object
    """
    return models.ManagerAccount(user_account=sample_user(email='manager@test.com'), belongs_to=belongs_to,
                                 employee_id=employee_id)


def sample_associate(belongs_to=sample_organisation(), employee_id='1234567809'):
    """
    Creates a sample associate account for testing
    :param user_account: User model object
    :param belongs_to: OrganisationAccount object
    :param employee_id: employee_id of associate
    :return: AssociateAccount object
    """
    return models.AssociateAccount(user_account=sample_user(email='assoc@test.com'),
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

        email = 'test@test.com'
        password = uuid.uuid4()
        full_name = 'test'
        nick_name = 'test'
        dob = '1998-09-01'
        user = get_user_model().objects.create_user(
            email=email, password=password, full_name=full_name,
            nick_name=nick_name, dob=dob)

        self.assertEqual(email, user.email)
        self.assertEqual(full_name, user.full_name)
        self.assertEqual(nick_name, user.nick_name)
        self.assertEqual(dob, user.dob)
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
        full_name = 'test'
        nick_name = 'test'
        dob = '1998-09-01'
        user = get_user_model().objects.create_user(
            email=email, password=password, full_name=full_name,
            nick_name=nick_name, dob=dob)

        self.assertEqual(email.lower(), user.email)

    def test_create_new_user_with_invalid_email_is_unsuccessful(self):
        """
        Test that user object is not created with an invalid email address
        :return: None
        """
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(
                email=None,
                password=uuid.uuid4(),
                full_name='test',
                nick_name='last_name',
                dob='1998-09-01'
            )

    def test_create_new_user_with_invalid_first_name_is_unsuccessful(self):
        """
        Test that user object is not created with an invalid first name
        :return: None
        """
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(
                email='test@test.com',
                password=uuid.uuid4(),
                full_name=None,
                nick_name='last_name',
                dob='1998-09-01'
            )

    def test_create_new_user_with_invalid_dob_is_unsuccessful(self):
        """
        Test that user object is not created with an invalid first name
        :return: None
        """
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(
                email='test@test.com',
                password=uuid.uuid4(),
                full_name='test',
                nick_name='last_name',
                dob=None
            )

    """
    Test if a superuser is created with valid details
    """
    def test_create_new_super_user_is_successful(self):
        """
        Test that a new super user is created
        :return: None
        """
        email = 'test@test.com'
        password = uuid.uuid4()
        full_name = 'test'
        nick_name = 'test'
        dob = '1998-09-01'
        user = get_user_model().objects.create_superuser(
            email=email, password=password, full_name=full_name,
            nick_name=nick_name, dob=dob)

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
