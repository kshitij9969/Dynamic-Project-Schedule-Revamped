from rest_framework.response import Response
from rest_framework import status

from core import models

"""
The functions(decorators) below check for hierarchical integrity i.e. the editing user must belong to the organisation.
"""


# def check_hierarchical_integrity_for_manager_update(update_manager_function):
#     """
#     Function(decorator) to check the following
#     1. If the logged in user is manager,
#     check the information provided is for his/her account OR
#     2. If the logged in user is an OrganisationAccount holder,
#     check if the account being update belongs to the organisation
#     :return: function object
#     """
#     def wrapper(*args, **kwargs):
#         """
#         Wrapper function
#         :param args: arguments
#         :param kwargs: key-worded arguments
#         :return: update_manager_function
#         """
#         request = args[1]
#         print(request.data)
#         is_allowed = False
#         username = request.data.get('user_account')['username']
#         logged_in_user = request.user
#         manager_instance = models.ManagerAccount.objects.filter(
#             user_account=models.User.objects.filter(
#                 username=username
#             ).first()).first()
#
#         if manager_instance == logged_in_user.manageraccount:
#             is_allowed = True
#
#         if hasattr(logged_in_user, 'organisationaccount') and \
#                 logged_in_user.organisationaccount.objects.filter(
#                     manageraccount=manager_instance).exists():
#             is_allowed = True
#
#         if not is_allowed:
#             return False
#
#     return wrapper
