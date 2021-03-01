from rest_framework import permissions

from core import models

USER_CHANGE_PERMISSIONS = [
    'change_user',
    'add_user',
    'delete_user',
    'change_user',
]

ORGANISATION_CRUD_PERMISSIONS = [
    'add_organisationaccount',
    'view_organisationaccount',
    'change_organisationaccount',
    'delete_organisationaccount',
]

MANAGER_CRUD_PERMISSIONS = [
    'add_manageraccount',
    'view_manageraccount',
    'change_manageraccount',
    'delete_manageraccount',
]

ASSOCIATE_CRUD_PERMISSIONS = [
    'add_associateaccount',
    'view_associateaccount',
    'change_associateaccount',
    'delete_associateaccount',
]


def prepend_app_name(app_name, list):
    """
    Preprends the app name at the begining of each element of the list
    :param app_name: String object
    :param list: List object
    :return: List object
    """
    return [(str(app_name) + '.' + str(elem)) for elem in list]

# Uncomment after adding model
# PROJECT_META_CRUD_PERMISSIONS = [
#     'core.view_project',
#     'core.update_associateaccount',
#     'core.delete_associateaccount',
# ]
#
# PROJECT_SCHEDULE_CRUD_PERMISSIONS = [
#     'core.view_'
# ]


class OrganisationPermissions(permissions.BasePermission):
    """
    Class for checking if the user has organisation crud permissions(all 4)
    """

    def has_permission(self, request, view):
        """
        Checks if account has Organisation CRUD permissions
        :param request: request object
        :param view:
        :return:
        """
        return True if request.user.has_perms(prepend_app_name('core', ORGANISATION_CRUD_PERMISSIONS) +
                               prepend_app_name('core', MANAGER_CRUD_PERMISSIONS) +
                               prepend_app_name('core', ASSOCIATE_CRUD_PERMISSIONS) + prepend_app_name('core', USER_CHANGE_PERMISSIONS)) \
            else False

"""

"""


class ManagerPermissions(permissions.BasePermission):
    """
    Class for checking if the user has organisation crud permissions(all 4)
    """

    def has_permission(self, request, view):
        """
        Checks if account has Organisation CRUD permissions
        :param request: request object
        :param view:
        :return:
        """
        has_permissions = request.user.has_perms(prepend_app_name('core', MANAGER_CRUD_PERMISSIONS) +
                                              prepend_app_name('core', ASSOCIATE_CRUD_PERMISSIONS) +
                                              prepend_app_name('core', USER_CHANGE_PERMISSIONS))

        return True if has_permissions else False
        
        # return True if the logged in user has permissions as well the hierarchical integrity is maintained


#
# class ManagerUpdateHierarchyIntegrityCheck(permissions.BasePermission):
#     """
#     Class for checking if the user has manager update permissions
#     """
#
#     def has_permission(self, request, view):
#         """
#         Checks the following
#         1. If the logged in user is manager,
#         check the information provided is for his/her account OR
#         2. If the logged in user is an OrganisationAccount holder,
#         check if the account being update belongs to the organisation
#         :param request:
#         :param view:
#         :return:
#         """
#         username = request.data.get('user_account')['username']
#         logged_in_user = request.user
#         manager_instance = models.ManagerAccount.objects.filter(
#             user_account=models.User.objects.filter(
#                 username=username
#             ).first()).first()
#
#         if manager_instance == logged_in_user.manageraccount:
#             del request.data.get('user_account')['username']
#             return True
#
#         if hasattr(logged_in_user, 'organisationaccount') and \
#                 logged_in_user.organisationaccount.objects.filter(
#                     manageraccount=manager_instance).exists():
#             del request.data.get('user_account')['username']
#             return True
#
#         del request.data.get('user_account')['username']
#         return False


class AssociatePermissions(permissions.BasePermission):
    """
    Class for checking if the user has organisation crud permissions(all 4)
    """

    def has_permission(self, request, view):
        """
        Checks if account has Organisation CRUD permissions
        :param request: request object
        :param view:
        :return:
        """
        return True if request.user.has_perms(prepend_app_name('core', ASSOCIATE_CRUD_PERMISSIONS) +
                                              prepend_app_name('core', USER_CHANGE_PERMISSIONS)) \
            else False