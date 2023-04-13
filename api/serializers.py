from rest_framework import serializers
from .models import User
from rest_framework.authtoken.models import Token
from drf_extra_fields.fields import Base64ImageField

class UserSerializer(serializers.ModelSerializer):
    image_profile = Base64ImageField(required=False)
    class Meta:
        model = User
        fields = ['id',
                'full_name',
                'preferred_name',
                'email',
                'password',
                'image_profile'
                ]

        extra_kwargs = {'password': {'write_only': True, 'required': True },
                        'image_profile': {'required': False, 'allow_blank': True, 'allow_null': True }}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        Token.objects.create(user=user)
        return user