from rest_framework import serializers

from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import ugettext_lazy as _

import uuid


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for User model
    """

    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'full_name',
                  'nick_name', 'password')
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
