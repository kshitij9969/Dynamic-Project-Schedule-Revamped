from rest_framework.authentication import (TokenAuthentication)
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.authtoken.models import Token as RestToken

from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _

import datetime, pytz


class MultiToken(RestToken):
    """
    Handles multiple tokens
    """
    key = models.CharField(_("Key"), max_length=40, db_index=True, unique=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="auth_token",
        on_delete=models.CASCADE, verbose_name=_("User")
    )
    device_identifier = models.CharField(_("DeviceIdentifier"), max_length=64)

    class Meta:
        unique_together = (("user", "device_identifier"),)


class OrgAccountTokenAuthentication(TokenAuthentication):
    """
    Handles token authentication for OrganisationAccount
    Note: All authentications are done using User model credentials(username and password),
    But the classes for token management is different for different types of accounts viz. OrganisationAccount,
    ManagerAccount, and AssociateAccount
    """
    def authenticate_credentials(self, key):
        """
        Authenticates credentials
        :param key:
        :return:
        """
        token_model = MultiToken
        try:
            token = token_model.objects.select_related("user").get(key=key)
        except token_model.DoesNotExist:
            raise AuthenticationFailed("Invalid token!")

        if not token.user.is_active:
            raise AuthenticationFailed("The user account is inactive!")

        utc_now = datetime.datetime.utcnow()
        utc_now = utc_now.replace(tzinfo=pytz.utc)

        if token.created < utc_now - datetime.timedelta(seconds=60):
            token.delete()
            raise AuthenticationFailed("Token expired!")

        return token.user, token


