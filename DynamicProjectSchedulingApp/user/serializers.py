from rest_framework import serializers

from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import ugettext_lazy as _

from core import models

from . import user_decorators


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for User model
    """

    class Meta:
        model = get_user_model()
        fields = ('username', 'full_name', 'nick_name',
                  'email', 'password')
        extra_kwargs = {
            'password': {'write_only': True, 'min_length': 8}
        }

    def create(self, validated_data):
        """
        Creates and returns User(Check core/models.py) object
        :param validated_data: validated data(fields of User object)
        :return: User object
        """
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        """
        Update the User object
        :param instance: User object
        :param validated_data: validated data(User class fields)
        :return: User object(updated object)
        """
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user


class AuthTokenSerializer(serializers.Serializer):
    """
    Serializer for user authentication
    """
    username = serializers.CharField(max_length=100)
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False
    )

    def validate(self, attrs):
        """
        Validate the user
        :param attrs: attributes(username and password)
        :return: attrs
        """
        username = attrs.get('username')
        password = attrs.get('password')

        user = authenticate(
            request=self.context.get('request'),
            username=username,
            password=password
        )

        if not user:
            msg = _('Unable to authenticate')
            raise serializers.ValidationError(msg, code='authenticate')

        attrs['user'] = user

        return attrs


class OrganisationAccountSerializer(serializers.ModelSerializer):
    """
    Serializer for OrganisationAccount model
    """
    user_account = UserSerializer(required=True, many=False)

    class Meta:
        model = models.OrganisationAccount
        exclude = ['account_verified',]

    def create(self, validated_data):
        """
        Creates and returns OrganisationAccount object
        :param validated_data: validated data(OrganisationAccount fields)
        :return: OrganisationAccount object
        """
        user_data = validated_data.pop('user_account')
        user_account = UserSerializer.create(UserSerializer(), validated_data=user_data)

        return models.OrganisationAccount.objects.create_org_account(
            user_account=user_account,
            **validated_data
        )

    def update(self, instance, validated_data):
        """
        Update the OrganisationAccount object
        :param instance: OrganisationAccount object
        :param validated_data: validated data(OrganisationAccount fields)
        :return: OrganisationAccount object
        """
        user_data = validated_data.pop('user_account')
        UserSerializer.update(UserSerializer(),
                              instance=self.context['request'].user,
                              validated_data=user_data)

        for (key, value) in validated_data.items():
            setattr(instance, key, value)
        instance.save()

        return instance


class ManagerAccountSerializer(serializers.ModelSerializer):
    """
    Serializer for OrganisationAccount model
    """
    user_account = UserSerializer(required=True, many=False)

    class Meta:
        model = models.ManagerAccount
        exclude = ['belongs_to',]

    def create(self, validated_data):
        """
        Creates and returns manager account
        :param validated_data: validated data(OrganisationAccount fields)
        :return: OrganisationAccount object
        """
        user_data = validated_data.pop('user_account')
        user_account = UserSerializer.create(UserSerializer(), validated_data=user_data)
        org_account = models.OrganisationAccount.objects.\
            filter(user_account=self.context['request'].user.id).first()

        return models.ManagerAccount.objects.create_manager_account(
            user_account=user_account,
            belongs_to=org_account,
            employee_id=validated_data['employee_id']
        )

    def update(self, instance, validated_data):
        """
        Updates and returns manager account
        :param instance: ManagerAccount object
        :param validated_data: validated data(OrganisationAccount fields)
        :return: OrganisationAccount object
        """
        user_data = validated_data.pop('user_account')
        UserSerializer.update(UserSerializer(),
                              instance=self.context['request'].user,
                              validated_data=user_data)

        for (key, value) in validated_data.items():
            setattr(instance, key, value)

        instance.save()

        return instance


class AssociateAccountSerializer(serializers.ModelSerializer):
    """
    Serializer for OrganisationAccount model
    """
    user_account = UserSerializer(required=True, many=False)

    class Meta:
        model = models.AssociateAccount
        exclude = ['belongs_to', 'reports_to']

    def create(self, validated_data):
        """
        Creates and returns manager account
        :param validated_data: validated data(OrganisationAccount fields)
        :return: OrganisationAccount object
        """
        user_data = validated_data.pop('user_account')
        user_account = UserSerializer.create(UserSerializer(), validated_data=user_data)

        manager_account = models.ManagerAccount.objects.\
            filter(user_account=self.context['request'].user.id).first()

        return models.ManagerAccount.objects.create_manager_account(
            user_account=user_account,
            belongs_to=manager_account.belongs_to,
            employee_id=validated_data['employee_id']
        )

    def update(self, instance, validated_data):
        """
        Updates and returns manager account
        :param instance: OrganisationAccount object
        :param validated_data: validated data(OrganisationAccount fields)
        :return: OrganisationAccount object
        """
        pass
