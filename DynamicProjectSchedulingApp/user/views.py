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


class ManageOrganisationAccountView(generics.RetrieveUpdateAPIView):
    """
    View to handle retrieval or updation of OrganisationAccount objects
    """
    serializer_class = OrganisationAccountSerializer
    authentication_classes = {tokens.OrgAccountTokenAuthentication}
    permission_classes = {permissions.IsAuthenticated, user_permission.OrganisationPermissions}

    def get_object(self):
        """
        Fetches and returns the OrganisationAccount object, if exists
        :return: None
        """
        return models.OrganisationAccount.objects.filter(user_account=self.request.user).first()


class CreateManagerAccountView(generics.CreateAPIView):
    """
    View to handle creation of ManagerAccount objects
    """
    serializer_class = ManagerAccountSerializer
    authentication_classes = {tokens.OrgAccountTokenAuthentication}
    permission_classes = {permissions.IsAuthenticated, user_permission.OrganisationPermissions}


class ManageManagerAccountView(generics.RetrieveUpdateAPIView):
    """
    View to handle updation and retrieval or ManagerAccount objects
    """
    serializer_class = ManagerAccountSerializer
    authentication_classes = {tokens.OrgAccountTokenAuthentication}
    permission_classes = {permissions.IsAuthenticated, user_permission.ManagerPermissions}

    def get_object(self):
        """
        Fetches and returns the ManagerAccount object, if exists
        :return: None
        """
        return models.ManagerAccount.objects.filter(user_account=self.request.user).first()


class CreateAssociateAccountView(generics.CreateAPIView):
    """
    View to handle creation of AssociateAccount objects
    """
    serializer_class = AssociateAccountSerializer
    authentication_classes = {tokens.OrgAccountTokenAuthentication}
    permission_classes = {permissions.IsAuthenticated, user_permission.ManagerPermissions}


class ManageAssociateAccountView(generics.RetrieveUpdateAPIView):
    """
    View to handle updation and retrieval of AssociateAccount objects
    """
    serializer_class = AssociateAccountSerializer
    authentication_classes = {tokens.OrgAccountTokenAuthentication}
    permission_classes = {permissions.IsAuthenticated, user_permission.AssociatePermissions}

    def get_object(self):
        """
        Fetches and returns AssociateAccount object if exist
        :return: None
        """
        return models.AssociateAccount.objects.filter(user_account=self.request.user).first()


class HomePageView(APIView):
    """
    View to handle homepage
    """
    authentication_classes = {tokens.OrgAccountTokenAuthentication}
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
                user_serializer = UserSerializer(request.user)
                org_serializer.data.pop('user_account')
                print(org_serializer.data)
                response = {**user_serializer.data}
                response.update(**org_serializer.data)

                managers = org_account.manageraccount_set.all()

                for manager in managers:
                    manager_serializer = ManagerAccountSerializer(manager)
                pass

            if hasattr(request.user, 'manageraccount'):
                pass

            if hasattr(request.user, 'associateaccount'):
                pass

        except Exception as e:
            pass

