from rest_framework import (generics, permissions, status)
from rest_framework.authtoken.views import ObtainAuthToken, APIView
from rest_framework.response import Response
from rest_framework import mixins

from user.serializers import (UserSerializer, AuthTokenSerializer,
                              OrganisationAccountSerializer,
                              ManagerAccountSerializer,
                              AssociateAccountSerializer)

from core import models

from . import tokens

import datetime

from . import user_permission

import json

# Helper functions


def flatten_user_account(account):
    """
    Helper function to flatten the user_account key
    in the dictionary
    :param account: Org account, Manager account
           or Associate account
    :return: Dictionary object
    """
    try:
        user_account = account['user_account']
        del account['user_account']
        account.update(user_account)

        return account
    except KeyError:
        pass


# Create your views here.


# class CreateUserView(generics.CreateAPIView):
#     """
#     View for creating user
#     """
#
#     serializer_class = UserSerializer


class LoginView(ObtainAuthToken):
    """
    View for creating token for user
    """

    def post(self, request, *args, **kwargs):
        """
        Handles HTTP POST request
        :param request: request object
        :param args:
        :param kwargs:
        :return:
        """
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            token, created = tokens.MultiToken.objects.get_or_create(
                user=serializer.validated_data['user'],
                device_identifier=request.data['device-identifier']
            )

            if not created:
                token.created = datetime.datetime.utcnow()
                token.save()

            return Response({'token': token.key, 'device-identifier': token.device_identifier})
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    """
    Handles logout
    """
    def get(self, request):
        """
        Handles HTTP GET request
        :param request: Request object
        :return:
        """
        request.auth.delete()
        return Response("User successfully logged out!")


# class ManageUserView(generics.RetrieveUpdateAPIView):
#     """
#     View to get a user profile
#     """
#     serializer_class = UserSerializer
#     authentication_classes = {tokens.OrgAccountTokenAuthentication}
#     permission_classes = {permissions.IsAuthenticated}
#
#     def get_object(self):
#         """
#         Fetch the profile of user, if authenticated
#         :return: User object
#         """
#         return self.request.user


class CreateOrganisationAccountView(generics.CreateAPIView):
    """
    View for creating OrganisationAccount object
    """
    serializer_class = OrganisationAccountSerializer


class UpdateOrganisationAccountView(generics.UpdateAPIView):
    """
    View to handle retrieval or updation of OrganisationAccount objects
    """
    serializer_class = OrganisationAccountSerializer
    authentication_classes = {tokens.MultiTokenAuthentication}
    permission_classes = {permissions.IsAuthenticated, user_permission.OrganisationPermissions}

    def get_object(self):
        """
        Fetch the object on which updation will happen
        :return: OrganisationAccount object
        """
        return models.OrganisationAccount.objects.filter(user_account=self.request.user).first()


class CreateManagerAccountView(generics.CreateAPIView):
    """
    View to handle creation of ManagerAccount objects
    """
    serializer_class = ManagerAccountSerializer
    authentication_classes = {tokens.MultiTokenAuthentication}
    permission_classes = {permissions.IsAuthenticated, user_permission.OrganisationPermissions}


class UpdateManagerAccountView(generics.UpdateAPIView):
    """
    View to handle updation and retrieval or ManagerAccount objects
    """
    serializer_class = ManagerAccountSerializer
    authentication_classes = {tokens.MultiTokenAuthentication}
    permission_classes = {permissions.IsAuthenticated, user_permission.ManagerPermissions}

    def get_object(self):
        """
        Fetch the object on which updation will happen
        :return: OrganisationAccount object
        """
        return models.ManagerAccount.objects.filter(user_account=self.request.user).first()


class CreateAssociateAccountView(APIView):
    """
    View to handle creation of AssociateAccount objects
    """
    authentication_classes = {tokens.MultiTokenAuthentication}
    permission_classes = {permissions.IsAuthenticated, user_permission.ManagerPermissions}

    def post(self, request):
        """
        Handles HTTP POST request
        :param request: Request object
        :return: Response
        """
        if hasattr(request.user, 'organisationaccount'):
            manager_account = models.ManagerAccount.objects.\
                filter(employee_id=request.data.pop('manager_employee_id')).first()

            if manager_account.belongs_to == request.user.organisationaccount:
                associate_serializer = AssociateAccountSerializer(data=request.data)

                if associate_serializer.is_valid():
                    user_data = request.data.pop('user_account')
                    user_account = UserSerializer.create(UserSerializer(), validated_data=user_data)
                    models.AssociateAccount.objects.create_associate_account(
                        user_account=user_account,
                        belongs_to=manager_account.belongs_to,
                        reports_to=manager_account,
                        employee_id=request.data.get('employee_id')
                    )

                    return Response(data=associate_serializer.data,
                                    status=status.HTTP_201_CREATED)

        if hasattr(request.user, 'manageraccount'):
            manager_account = models.ManagerAccount.objects.filter(user_account=request.user).first()
            associate_serializer = AssociateAccountSerializer(data=request.data)

            if associate_serializer.is_valid():
                user_data = request.data.pop('user_account')
                user_account = UserSerializer.create(UserSerializer(), validated_data=user_data)
                models.AssociateAccount.objects.create_associate_account(
                    user_account=user_account,
                    belongs_to=manager_account.belongs_to,
                    reports_to=manager_account,
                    employee_id=request.data.get('employee_id')
                )

                return Response(data=associate_serializer.data,
                                status=status.HTTP_201_CREATED)

        return Response(data={'Bad request!'},
                        status=status.HTTP_400_BAD_REQUEST)


class UpdateAssociateAccountView(generics.UpdateAPIView):
    """
    View to handle updation and retrieval of AssociateAccount objects
    """
    serializer_class = AssociateAccountSerializer
    authentication_classes = {tokens.MultiTokenAuthentication}
    permission_classes = {permissions.IsAuthenticated, user_permission.AssociatePermissions}

    def get_object(self):
        """
        Fetch the object on which updation will happen
        :return: OrganisationAccount object
        """
        return models.AssociateAccount.objects.filter(user_account=self.request.user).first()


class HomePageView(APIView):
    """
    View to handle homepage
    """
    authentication_classes = {tokens.MultiTokenAuthentication}
    permission_classes = {permissions.IsAuthenticated,}

    def get(self, request):
        """
        Handles HTTP GET request
        :param request: Request object
        :return: Response object
        """
        response = {}
        try:

            if hasattr(request.user, 'organisationaccount'):
                org_account = request.user.organisationaccount
                org_serializer = OrganisationAccountSerializer(org_account)
                org_data = flatten_user_account(org_serializer.data)

                response = {**org_data}
                response['managers'] = []
                response['associates'] = []

                managers = org_account.manageraccount_set.all()
                associates = org_account.associateaccount_set.all()

                for manager in managers:
                    manager_serializer = ManagerAccountSerializer(manager)
                    response['managers'].append(flatten_user_account(manager_serializer.data))

                for associate in associates:
                    associate_serializer = AssociateAccountSerializer(associate)
                    response['associates'].append(flatten_user_account(associate_serializer.data))

                # response = json.dumps(response)

                return Response(data=response, status=status.HTTP_200_OK)

            if hasattr(request.user, 'manageraccount'):
                manager_account = request.user.manageraccount
                manager_serializer = ManagerAccountSerializer(manager_account)
                manager_data = flatten_user_account(manager_serializer.data)

                response = {**manager_data}
                response['organisation'] = []
                response['associates'] = []
                response['projects'] = []

                organisation = manager_account.belongs_to
                associates = manager_account.associateaccount_set.all()

                for associate in associates:
                    associate_serializer = AssociateAccountSerializer(associate)
                    response['associates'].append(flatten_user_account(associate_serializer.data))

                organisation_serializer = OrganisationAccountSerializer(organisation)

                response['organisation'].append(flatten_user_account(organisation_serializer.data))

                # response = json.dumps(response)

                return Response(data=response, status=status.HTTP_200_OK)

            if hasattr(request.user, 'associateaccount'):
                associate_account = request.user.associateaccount
                associate_serializer = AssociateAccountSerializer(associate_account)
                associate_data = flatten_user_account(associate_serializer.data)

                response = {**associate_data}
                response['organisation'] = []
                response['manager'] = []
                response['projects'] = []

                organisation = associate_account.belongs_to
                manager = associate_account.reports_to

                organisation_serializer = OrganisationAccountSerializer(organisation)
                manager_serializer = ManagerAccountSerializer(manager)

                response['organisation'].append(flatten_user_account(organisation_serializer.data))
                response['manager'].append(flatten_user_account(manager_serializer.data))

                # response = (response)

                return Response(data=response, status=status.HTTP_200_OK)

            return Response(data={'response': 'user not associated with any account!'},
                            status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response(data={'response': 'bad request'},
                            status=status.HTTP_400_BAD_REQUEST)


class GetManagerListApi(APIView):
    """
    View handles fetching list of managers belonging to an organisation
    """
    authentication_classes = {tokens.MultiTokenAuthentication}
    permission_classes = {permissions.IsAuthenticated,
                          user_permission.OrganisationPermissions}

    def get(self, request):
        """
        Handles HTTP GET method
        :param request: Request object
        :return: Response object
        """
        response = dict()
        response['managers'] = []
        org_account = self.request.user.organisationaccount

        manager_list = org_account.manageraccount_set.all()

        for manager in manager_list:
            manager_serializer = ManagerAccountSerializer(manager)
            response['managers'].append(flatten_user_account(manager_serializer.data))

        return Response(data=response, status=status.HTTP_200_OK)


class GetAssociateListApi(APIView):
    """
    View handles fetching list of associates belonging to an organisation or reporting to a manager
    """
    authentication_classes = {tokens.MultiTokenAuthentication}
    permission_classes = {permissions.IsAuthenticated, user_permission.ManagerPermissions}

    def get(self, request):
        """
        Handles HTTP GET request
        :param request: Request object
        :return: Response object
        """
        response = dict()
        response['associates'] = []

        if hasattr(self.request.user, 'organisationaccount'):
            org_account = self.request.user.organisationaccount

            associate_list = org_account.associateaccount_set.all()

            for associate in associate_list:
                associate_serializer = AssociateAccountSerializer(associate)
                response['associates'].append(flatten_user_account(associate_serializer.data))

            return Response(data=response, status=status.HTTP_200_OK)

        if hasattr(self.request.user, 'manageraccount'):
            manager_account = self.request.user.manageraccount

            associate_list = manager_account.associateaccount_set.all()

            for associate in associate_list:
                associate_serializer = AssociateAccountSerializer(associate)
                response['associates'].append(flatten_user_account(associate_serializer.data))

            return Response(data=response, status=status.HTTP_200_OK)


class DeleteOrganisationViewApi(APIView):
    """
    Handles deletion of all accounts
    """
    authentication_classes = {tokens.MultiTokenAuthentication}
    permission_classes = {permissions.IsAuthenticated,
                          user_permission.OrganisationPermissions}

    def delete(self, request):
        """
        Handles HTTP DELETE request
        :param request: Request object
        :return: Response object
        """
        org_account = self.request.user.organisationaccount
        associate_account = org_account.associateaccount_set.all()
        manager_account = org_account.manageraccount_set.all()

        # First delete associates

        for associate in associate_account:
            user = associate.user_account
            user.delete()

        # Then delete managers
        for manager in manager_account:
            user = manager.user_account
            user.delete()

        # Finally delete organisation account
        self.request.user.delete()

        return Response(data={'Account delete successfully'},
                        status=status.HTTP_200_OK)


class DeleteManagerViewApi(APIView):
    """
    View to handle deletion of ManagerAccount
    """
    authentication_classes = {tokens.MultiTokenAuthentication}
    permission_classes = {permissions.IsAuthenticated,
                          user_permission.OrganisationPermissions}

    def delete(self, request):
        """
        Handles HTTP DELETE request
        :param request: Request object
        :return: Response object
        """
        username = request.data.get('username')
        org_account = self.request.user.organisationaccount
        user_account = models.User.objects.filter(username=username).first()

        if user_account is not None:
            if hasattr(user_account, 'manageraccount'):
                manager_account = user_account.manageraccount
            else:
                return Response(data={'User is not associated with a manager account!'},
                                status=status.HTTP_400_BAD_REQUEST)

            if manager_account in org_account.manageraccount_set.all():
                associates = manager_account.associateaccount_set.all()
                for associate in associates:
                    associate_user = associate.user_account
                    associate_user.delete()

                user_account.delete()
                return Response(data={'Manager successfully deleted!'},
                                status=status.HTTP_200_OK)

        return Response(data={'User does not exist!'},
                        status=status.HTTP_400_BAD_REQUEST)


class DeleteAssociateViewApi(APIView):
    """
    View to handle deletion of AssociateAccount
    """
    authentication_classes = {tokens.MultiTokenAuthentication}
    permission_classes = {permissions.IsAuthenticated,
                          user_permission.ManagerPermissions}

    def delete(self, request):
        """
        Handles HTTP DELETE request
        :param request: Request object
        :return: Response object
        """
        username = request.data.get('username')
        associate_user = models.User.objects.filter(username=username).first()

        if associate_user is not None\
                and hasattr(associate_user, 'associateaccount'):
            if hasattr(self.request.user, 'organisationaccount'):
                associate_account = associate_user.associateaccount
                org_account = self.request.user.organisationaccount
                if associate_account in org_account.associateaccount_set.all():
                    associate_user.delete()

                    return Response(data={'User account deleted!'},
                                    status=status.HTTP_200_OK)

            if hasattr(self.request.user, 'manageraccount'):
                associate_account=associate_user.associateaccount
                manager_account = self.request.user.manageraccount
                if associate_account in manager_account.associateaccount_set.all():
                    associate_user.delete()

                    return Response(data={'User account deleted!'},
                                    status=status.HTTP_200_OK)

        return Response(data={'User account does not exist!'},
                        status=status.HTTP_400_BAD_REQUEST)


class GetMyProfileApi(APIView):
    """
    View to fetch profile
    """
    authentication_classes = {tokens.MultiTokenAuthentication}
    permission_classes = {permissions.IsAuthenticated}

    def get(self, request):
        """
        Handles HTTP GET request
        :param request: Request object
        :return: Response object
        """
        response = dict()
        if hasattr(self.request.user, 'organisationaccount'):
            org_account = self.request.user.organisationaccount
            org_serializer = OrganisationAccountSerializer(org_account)

            response = flatten_user_account(org_serializer.data)

            return Response(data=response, status=status.HTTP_200_OK)

        if hasattr(self.request.user, 'manageraccount'):
            manager_account = self.request.user.manageraccount
            manager_serializer = ManagerAccountSerializer(manager_account)

            response = flatten_user_account(manager_serializer.data)

            return Response(data=response, status=status.HTTP_200_OK)

        if hasattr(self.request.user, 'associateaccount'):
            associate_account = self.request.user.associateaccount
            associate_serializer = AssociateAccountSerializer(associate_account)

            response = flatten_user_account(associate_serializer.data)

            return Response(data=response, status=status.HTTP_200_OK)

        return Response(data={'Account does not exists!'},
                        status=status.HTTP_400_BAD_REQUEST)


class ResetPasswordApi(APIView):
    """
    View to handle password reset
    """
    authentication_classes = {tokens.MultiTokenAuthentication}
    permission_classes = {permissions.IsAuthenticated}

    def post(self, request):
        user_account = self.request.user
        if user_account.check_password(request.data.get('current_password')):
            user_account.set_password(request.data.get('new_password'))

            token_list = tokens.MultiToken.objects.filter(user=user_account)
            for token in token_list:
                token.delete()

            user_account.save()

            return Response(data={'Password changed!'},
                            status=status.HTTP_200_OK)

        return Response(data={'Bad request!'},
                        status=status.HTTP_400_BAD_REQUEST)

