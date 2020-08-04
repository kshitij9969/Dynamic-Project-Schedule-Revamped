# from django.test import TestCase
# from django.contrib.auth import get_user_model
# from django.urls import reverse
# from django.contrib.auth import login
#
# from rest_framework.test import APIClient
# from rest_framework import status
#
# from PIL import Image
#
# from core import models
# from core.test.test_model import get_sample_employee_id
#
# import uuid, copy
#
# from faker import Faker
#
# CREATE_USER_URL = reverse('user:create')
# TOKEN_URL = reverse('user:token')
# ME_URL = reverse('user:me')
#
# CREATE_ORG_URL = reverse('user:create-org')
# ORG_ME_URL = reverse('user:me-org')
#
# CREATE_MANAGER_URL = reverse('user:create-manager')
# MANAGER_ME_URL = reverse('user:me-manager')
#
# CREATE_ASSOCIATE_URL = reverse('user:create-associate')
# ASSOCIATE_ME_URL = reverse('user:me-associate')
#
# fake = Faker()
#
# SAMPLE_USER_PAYLOAD = {
#     'username': str(uuid.uuid4()),
#     'full_name': fake.name(),
#     'nick_name': fake.name(),
#     'email': fake.company_email(),
#     'password': fake.password(),
# }
#
# SAMPLE_ORG_PAYLOAD = {**SAMPLE_USER_PAYLOAD, **{
#     'industry': 'IT',
#     'country_code': fake.country_calling_code(),
#     'contact_no': fake.phone_number(),
#     'address_line_one': fake.street_name(),
#     'address_line_two': fake.street_name(),
#     'country': fake.country(),
#     'province_state': 'Maharashtra',
#     'city': fake.city()
# }}
#
# SAMPLE_ORG_ONLY_PAYLOAD = {
#     'industry': 'IT',
#     'country_code': fake.country_calling_code(),
#     'contact_no': fake.phone_number(),
#     'address_line_one': fake.street_name(),
#     'address_line_two': fake.street_name(),
#     'country': fake.country(),
#     'province_state': 'Maharashtra',
#     'city': fake.city()
# }
#
# SAMPLE_MANAGER_PAYLOAD = {
#         'user_account':{
#             'username': uuid.uuid4(),
#             'full_name': fake.name(),
#             'nick_name': fake.name(),
#             'email': fake.company_email(),
#             'password': fake.password()
#                        },
#         **{'employee_id': get_sample_employee_id(),}
# }
#
#
# SAMPLE_ASSOCIATE_ACCOUNT_PAYLOAD = {
#         'user_account': {
#             'username': uuid.uuid4(),
#             'full_name': fake.name(),
#             'nick_name': fake.name(),
#             'email': fake.company_email(),
#             'password': fake.password()
#                        },
#         **{'employee_id': get_sample_employee_id(),}
# }
#
#
# def create_user(**params):
#     """
#     Helper function to create user
#     :param params: parameters to create User object
#     :return: User object
#     """
#     return get_user_model().objects.create_user(**params)
#
#
# def create_organisation(**params):
#     """
#     Helper function to create OrganisationAccount object
#     :param params: parameters to create OrganisationAccount object
#     :return: OrganisationAccount object
#     """
#     return models.OrganisationAccount.objects.\
#         create_org_account(**params)
#
#
# def create_manager(**params):
#     """
#     Helper function to create ManagerAccount object
#     :param params: parameters to create ManagerAccount object
#     :return: ManagerAccount object
#     """
#     return models.ManagerAccount.objects.create_manager_account(**params)
#
#
# def create_associate(**params):
#     """
#     Helper function to create AssociateAccount object
#     :param params: parameters to create AssociateAccount object
#     :return: AssociateAccount object
#     """
#     return models.AssociateAccount.objects.create_associate_account(**params)
#
#
# class PublicUserApiTest(TestCase):
#     """
#     Test the public APIs for User app
#     """
#     def setUp(self) -> None:
#         """
#         Setup for the test
#         :return: None
#         """
#         self.api_client = APIClient()
#
#     def test_create_user_with_valid_credentials(self):
#         """
#         Test that User object can be created using the API
#         :return: None
#         """
#         res = self.api_client.post(CREATE_USER_URL, SAMPLE_USER_PAYLOAD)
#         user = get_user_model().objects.get(**res.data)
#
#         self.assertEqual(res.status_code, status.HTTP_201_CREATED)
#         self.assertTrue(user.check_password(SAMPLE_USER_PAYLOAD['password']))
#         self.assertNotIn('password', res.data)
#
#     def test_user_exists(self):
#         """
#         Test that multiple user accounts cannot be created with same credentials
#         :return: None
#         """
#         create_user(**SAMPLE_USER_PAYLOAD)
#
#         res = self.api_client.post(CREATE_USER_URL, SAMPLE_USER_PAYLOAD)
#
#         self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
#
#     def test_password_strength(self):
#         """
#         Test that password is at least 8 characters long
#         :return: None
#         """
#         payload = copy.deepcopy(SAMPLE_USER_PAYLOAD)
#         payload.update(password='test')
#
#         res = self.api_client.post(CREATE_USER_URL, payload)
#         user_exist = get_user_model().objects.filter(**res.data).exists()
#
#         self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
#         self.assertFalse(user_exist)
#
#     def test_create_token_for_user_is_successful(self):
#         """
#         Test that a token can be created for a user using TOKEN_URL(see top)
#         :return: None
#         """
#         create_user(**SAMPLE_USER_PAYLOAD)
#         TOKEN_PAYLOAD = {
#             'username': SAMPLE_USER_PAYLOAD['username'],
#             'password': SAMPLE_USER_PAYLOAD['password'],
#             'device-identifier': str(uuid.uuid4())
#         }
#
#         res = self.api_client.post(TOKEN_URL, TOKEN_PAYLOAD)
#
#         self.assertEqual(res.status_code, status.HTTP_200_OK)
#         self.assertIn('token', res.data)
#         self.assertEqual(TOKEN_PAYLOAD['device-identifier'],
#                          res.data['device-identifier'])
#
#     def test_create_token_with_invalid_credentials_is_unsuccessful(self):
#         """
#         Test that token cannot be created with invalid credentials
#         :return: None
#         """
#         create_user(**SAMPLE_USER_PAYLOAD)
#
#         TOKEN_PAYLOAD = {
#             'username': SAMPLE_USER_PAYLOAD['username'],
#             'password': 'wrong_password',
#             'device-identifier': str(uuid.uuid4())
#         }
#
#         res = self.api_client.post(TOKEN_URL, TOKEN_PAYLOAD)
#
#         self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
#         self.assertNotIn('token', res.data)
#         self.assertNotIn('device-identifier', res.data)
#
#     def test_create_token_without_user(self):
#         """
#         Test that a token cannot be created without a user account
#         :return: None
#         """
#         res = self.api_client.post(TOKEN_URL, SAMPLE_USER_PAYLOAD)
#
#         self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
#
#     def test_create_token_with_missing_fields_is_unsuccessful(self):
#         """
#         Test that a token cannot be created with fields missing
#         :return: None
#         """
#         payload = copy.deepcopy(SAMPLE_USER_PAYLOAD)
#
#         del payload['password']
#
#         res = self.api_client.post(TOKEN_URL, payload)
#
#         self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
#         self.assertNotIn('token', res.data)
#
#     def test_retrieve_user_unauthorized_is_unsuccessful(self):
#         """
#         Test that a user profile cannot be retrieve without authorization
#         :return: None
#         """
#         res = self.api_client.post(ME_URL)
#
#         self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
#
#
# class PrivateUserApiTest(TestCase):
#     """
#     Class for testing private API of User model
#     """
#     def setUp(self) -> None:
#         """
#         Set up for the following tests
#         :return: None
#         """
#         self.user = create_user(**SAMPLE_USER_PAYLOAD)
#         self.api_client = APIClient()
#         self.api_client.force_authenticate(user=self.user)
#
#     def test_retrieve_user_detail_is_successful(self):
#         """
#         Test that an authenticated user can retrieve profile
#         :return: None
#         """
#         res = self.api_client.get(ME_URL)
#         expected_res = copy.deepcopy(SAMPLE_USER_PAYLOAD)
#         del expected_res['password']
#
#         self.assertEqual(res.status_code, status.HTTP_200_OK)
#         self.assertEqual(res.data, expected_res)
#
#     def test_retrieve_user_detail_using_post_fails(self):
#         """
#         Test that post method is not allowed for
#         retrieving user profile
#         :return: None
#         """
#         res = self.api_client.post(ME_URL)
#
#         self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
#
#     def test_update_user_profile(self):
#         """
#         Test that profile can be update using
#         :return: None
#         """
#         update_payload = copy.deepcopy(SAMPLE_USER_PAYLOAD)
#         update_payload['email'] = 'newemail@test.com'
#         update_payload['full_name'] = 'new_full_name'
#         update_payload['nick_name'] = 'new_nick_name'
#         update_payload['username'] = 'new_user_name'
#
#         res = self.api_client.patch(ME_URL, update_payload)
#         self.user.refresh_from_db()
#
#         self.assertEqual(res.status_code, status.HTTP_200_OK)
#         self.assertEqual(self.user.email, update_payload['email'])
#         self.assertEqual(self.user.full_name, update_payload['full_name'])
#         self.assertEqual(self.user.nick_name, update_payload['nick_name'])
#         self.assertEqual(self.user.username, update_payload['username'])
#
#
# class OrganisationAccountPublicApiTest(TestCase):
#     """
#     Test cases for public APIs of OrganisationAccount model
#     """
#     def setUp(self) -> None:
#         """
#         Set up for the following tests
#         :return: None
#         """
#         self.api_client = APIClient()
#
#     def test_new_org_account_is_created_successfully(self):
#         """
#         Test that a new OrganisationAccount is created successfully
#         :return: None
#         """
#         SAMPLE_ORG_PAYLOAD = {
#             'user_account': {
#                 'username': str(uuid.uuid4()),
#                 'full_name': fake.name(),
#                 'nick_name': fake.name(),
#                 'email': fake.company_email(),
#                 'password': fake.password()
#             },
#             'industry': 'IT',
#             'country_code': fake.country_calling_code(),
#             'contact_no': fake.phone_number(),
#             'address_line_one': fake.street_name(),
#             'address_line_two': fake.street_name(),
#             'country': fake.country(),
#             'province_state': 'Maharashtra',
#             'city': fake.city()
#         }
#
#         res = self.api_client.post(CREATE_ORG_URL, SAMPLE_ORG_PAYLOAD, format='json')
#
#         user = get_user_model().objects.get(**(res.data.pop('user_account')))
#         org_account = models.OrganisationAccount.objects.get(**res.data)
#
#         self.assertEqual(res.status_code, status.HTTP_201_CREATED)
#         self.assertIsNotNone(user)
#         self.assertIsNotNone(org_account)
#         self.assertNotIn('password', res.data)
#
#     def test_organisation_account_login_is_successful(self):
#         """
#         Test that organisation account login is successful
#         :return: None
#         """
#         pass
#
#
# class PrivateOrganisationAccountApiTest(TestCase):
#     """
#     Class to test the private APIs for OrganisationAccount model.
#     Test that organisation account is
#     1. Able to create manager
#     2. Update a manager
#     3. Delete a manager
#     4. View a manager
#     5. View an associate
#     6. Update an associate
#     7. Delete an associate
#     8. Fetch details about organisation account(itself)
#
#
#     only when authentication is successful
#     and unable to
#     1. Create other organisation accounts
#     2. Update other organisations
#     3. Delete other organisations
#     4. View other organisations' details
#     5. Create associates
#     6. Perform CRUD on managers from other organisations
#     7. Perform CRUD on associates from other organisations
#
#     """
#     def setUp(self) -> None:
#         """
#         Set up for the following tests
#         :return: None
#         """
#         self.api_client = APIClient()
#         self.user = create_user(**SAMPLE_USER_PAYLOAD)
#         self.org = create_organisation(user_account=self.user, **SAMPLE_ORG_ONLY_PAYLOAD)
#         self.user.refresh_from_db()
#
#     def test_retrieve_org_profile_is_successful(self):
#         """
#         Test that OrganisationAccount details can be retrieved successfully
#         :return: None
#         """
#         self.api_client.force_authenticate(user=self.user)
#         res = self.api_client.get(ORG_ME_URL)
#         self.assertEqual(res.status_code, status.HTTP_200_OK)
#         self.assertEqual(res.data['user_account']['username'], self.user.username)
#         self.assertEqual(res.data['city'], self.org.city)
#
#     def test_post_org_profile_not_allowed(self):
#         """
#         Test that post method is not allowed to be called on ORG_ME_URL
#         :return: None
#         """
#         self.api_client.force_authenticate(user=self.user)
#         res = self.api_client.post(ORG_ME_URL)
#         self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
#
#     def test_update_org_account_is_successful(self):
#         """
#         Test that OrganisationAccount can be updated successfully
#         :return: None
#         """
#         SAMPLE_ORG_PAYLOAD = {
#             'user_account': {
#                 'full_name': 'dummy_full_name',
#                 'nick_name': 'dummy_nick_name',
#                 'email': 'fakeemail@test.com',
#             },
#             'industry': 'Manufacturing',
#             'country_code': '+91',
#             'contact_no': '1234566789',
#             'address_line_one': 'dummy_line_one',
#             'address_line_two': 'dummy_line_two',
#             'country': 'India',
#             'province_state': 'Maharashtra',
#             'city': 'Mumbai'
#         }
#         self.api_client.force_authenticate(user=self.user)
#
#         res = self.api_client.patch(ORG_ME_URL, SAMPLE_ORG_PAYLOAD, format='json')
#         self.user.refresh_from_db()
#         self.org.refresh_from_db()
#
#         self.assertEqual(res.status_code, status.HTTP_200_OK)
#
#     def test_get_org_account_detail_without_authentication_is_unsuccessful(self):
#         """
#         Test that OrganisationAccount information cannot be fetched without login
#         :return: None
#         """
#         TEMP_USER_PAYLOAD = copy.deepcopy(SAMPLE_USER_PAYLOAD)
#         TEMP_USER_PAYLOAD['username'] = uuid.uuid4()
#         temp_user = create_user(**TEMP_USER_PAYLOAD)
#         create_organisation(user_account=temp_user, **SAMPLE_ORG_ONLY_PAYLOAD)
#
#         res = self.api_client.get(ORG_ME_URL)
#         self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
#         self.assertNotIn('username', res.data)
#
#
# class PrivateManagerApiTest(TestCase):
#     """
#     Class for testing private Api of ManagerAccount
#     Class to test the private APIs for OrganisationAccount model.
#     Test that organisation account is
#     2. Update a manager(itself)
#     4. View a manager(itself and others but
#                       within the organisation)
#     5. View an associate(only the ones reporting to him)
#     6. Update an associate(only the ones reporting to him)
#     7. Delete an associate(only the ones reporting to him)
#     8. Fetch details about organisation account(itself)
#
#     only when authentication is successful
#     """
#     def setUp(self) -> None:
#         self.api_client = APIClient()
#         self.org_user = create_user(**SAMPLE_USER_PAYLOAD)
#         self.org = create_organisation(user_account=self.org_user, **SAMPLE_ORG_ONLY_PAYLOAD)
#         self.org_user.refresh_from_db()
#
#     def test_manager_account_create_is_successful(self):
#         """
#         Test that a manager account can be created successfully
#         :return: None
#         """
#         self.api_client.force_authenticate(user=self.org_user)
#
#         res = self.api_client.post(CREATE_MANAGER_URL, SAMPLE_MANAGER_PAYLOAD, format='json')
#
#         user = get_user_model().objects.get(**res.data.pop('user_account'))
#         manager = models.ManagerAccount.objects.get(**res.data)
#
#         self.assertEqual(res.status_code, status.HTTP_201_CREATED)
#         self.assertNotIn('password', res.data)
#         self.assertIsNotNone(user)
#         self.assertIsNotNone(manager)
#
#     def test_manager_account_retrieve_is_successful(self):
#         """
#         Test that a manage account details can be retrieved successfully
#         :return: None
#         """
#         manager_user = create_user(**{
#             'username': uuid.uuid4(),
#             'email': fake.company_email(),
#             'full_name': fake.name(),
#             'nick_name': fake.name(),
#             'password': fake.password()
#         })
#
#         sample_org_user = create_user(**{
#             'username': uuid.uuid4(),
#             'email': fake.company_email(),
#             'full_name': fake.name(),
#             'nick_name': fake.name(),
#             'password': fake.password()
#         })
#         manager_org = create_organisation(user_account=sample_org_user, **SAMPLE_ORG_ONLY_PAYLOAD)
#         manager = create_manager(user_account=manager_user,
#                                  belongs_to=manager_org,
#                                  employee_id=get_sample_employee_id())
#
#         self.api_client.force_authenticate(user=manager_user)
#
#         res = self.api_client.get(MANAGER_ME_URL)
#
#         self.assertEqual(res.status_code, status.HTTP_200_OK)
#         self.assertNotIn('password', res.data)
#         self.assertEqual(str(manager.employee_id), res.data['employee_id'])
#
#     def test_update_manage_account_is_successful(self):
#         """
#         Test that the manager account can be updated successfully
#         :return: None
#         """
#         manager_username = uuid.uuid4(),
#         manager_user = create_user(**{
#             'username': manager_username,
#             'email': fake.company_email(),
#             'full_name': fake.name(),
#             'nick_name': fake.name(),
#             'password': fake.password()
#         })
#
#         sample_org_user = create_user(**{
#             'username': manager_username,
#             'email': fake.company_email(),
#             'full_name': fake.name(),
#             'nick_name': fake.name(),
#             'password': fake.password()
#         })
#         manager_org = create_organisation(user_account=sample_org_user, **SAMPLE_ORG_ONLY_PAYLOAD)
#         manager = create_manager(user_account=manager_user,
#                                  belongs_to=manager_org,
#                                  employee_id=get_sample_employee_id())
#
#         self.api_client.force_authenticate(user=manager_user)
#
#         sample_update_manager_payload = {
#             'user_account': {
#                 'username': manager_username,
#                 'full_name': 'test_full_name',
#                 'last_name': 'test_nick_name',
#                 'email': 'test@test.com',
#             },
#             'employee_id': '111111111',
#         }
#
#         res = self.api_client.patch(MANAGER_ME_URL,
#                                     sample_update_manager_payload,
#                                     format='json')
#
#         self.assertEqual(res.status_code, status.HTTP_200_OK)
#         self.assertNotIn('password', res.data)
#
#     def test_update_manage_account_by_org_is_successful(self):
#         """
#         Test that the manager account can be updated successfully
#         :return: None
#         """
#         manager_username = uuid.uuid4(),
#         manager_user = create_user(**{
#             'username': manager_username,
#             'email': fake.company_email(),
#             'full_name': fake.name(),
#             'nick_name': fake.name(),
#             'password': fake.password()
#         })
#
#         sample_org_user = create_user(**{
#             'username': manager_username,
#             'email': fake.company_email(),
#             'full_name': fake.name(),
#             'nick_name': fake.name(),
#             'password': fake.password()
#         })
#         manager_org = create_organisation(user_account=sample_org_user, **SAMPLE_ORG_ONLY_PAYLOAD)
#         manager = create_manager(user_account=manager_user,
#                                  belongs_to=manager_org,
#                                  employee_id=get_sample_employee_id())
#
#         self.api_client.force_authenticate(user=sample_org_user)
#
#         sample_update_manager_payload = {
#             'user_account': {
#                 'username': manager_username,
#                 'full_name': 'test_full_name',
#                 'last_name': 'test_nick_name',
#                 'email': 'test@test.com',
#             },
#             'employee_id': '111111111',
#         }
#
#         res = self.api_client.patch(MANAGER_ME_URL,
#                                     sample_update_manager_payload,
#                                     format='json')
#
#         self.assertEqual(res.status_code, status.HTTP_200_OK)
#         self.assertNotIn('password', res.data)
#
#
# class PrivateAssociateApiTest(TestCase):
#     """
#     Class for testing private APIs of Associate account
#     """
#
#     def setUp(self) -> None:
#         """
#         Setup for following tests
#         :return: None
#         """
#         self.api_client = APIClient()
#         self.org_user = create_user(**{
#             'username': uuid.uuid4(),
#             'email': fake.company_email(),
#             'full_name': fake.name(),
#             'nick_name': fake.name(),
#             'password': fake.password()
#         })
#         self.manager_user = create_user(**{
#             'username': uuid.uuid4(),
#             'email': fake.company_email(),
#             'full_name': fake.name(),
#             'nick_name': fake.name(),
#             'password': fake.password()
#         })
#         self.org_account = create_organisation(user_account=self.org_user,
#                                                **SAMPLE_ORG_ONLY_PAYLOAD)
#         self.manager_account = create_manager(user_account=self.manager_user,
#                                               belongs_to=self.org_account,
#                                               employee_id=get_sample_employee_id())
#
#     def test_associate_account_is_created_successfully(self):
#         """
#         Test that an associate account can be created successfully
#         :return: None
#         """
#         self.api_client.force_authenticate(user=self.manager_user)
#
#         res = self.api_client.post(
#             CREATE_ASSOCIATE_URL,
#             SAMPLE_ASSOCIATE_ACCOUNT_PAYLOAD,
#             format='json'
#         )
#
#     def test_associate_account_retrieve_is_successful(self):
#         """
#         Test that an associate account can be retrieved successfully
#         :return: None
#         """
#         associate_user = create_user(**{
#             'username': uuid.uuid4(),
#             'email': fake.company_email(),
#             'full_name': fake.name(),
#             'nick_name': fake.name(),
#             'password': fake.password()
#         })
#         org_user = create_user(
#             **{
#                 'username': uuid.uuid4(),
#                 'email': fake.company_email(),
#                 'full_name': fake.name(),
#                 'nick_name': fake.name(),
#                 'password': fake.password()
#             }
#         )
#         manager_user = create_user(
#             **{
#                 'username': uuid.uuid4(),
#                 'email': fake.company_email(),
#                 'full_name': fake.name(),
#                 'nick_name': fake.name(),
#                 'password': fake.password()
#             }
#         )
#         org_account = create_organisation(user_account=org_user,
#                                           **SAMPLE_ORG_ONLY_PAYLOAD)
#         manager_account = create_manager(user_account=manager_user,
#                                          belongs_to=org_account,
#                                          employee_id=get_sample_employee_id())
#
#         associate = create_associate(user_account=associate_user,
#                                      employee_id=get_sample_employee_id(),
#                                      reports_to=manager_account,
#                                      belongs_to=org_account)
#         self.api_client.force_authenticate(user=associate_user)
#
#         res = self.api_client.get(ASSOCIATE_ME_URL)
#
#
#
#
#
