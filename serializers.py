from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from .models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['user_type', 'phone', 'birth_date', 'bio', 'avatar_url']


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    profile = ProfileSerializer()

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'password',
            'email',
            'first_name',
            'last_name',
            'profile',
        ]
        extra_kwargs = {'password': {'write_only': True, 'required': True}}

    def validate_password(self, value):
        validate_password(value)
        return value

    def create(self, validated_data):
        profile_data = validated_data.pop('profile')
        user = User.objects.create_user(**validated_data)
        Profile.objects.create(user=user, **profile_data)
        return user

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile', None)
        password = validated_data.pop('password', None)

        for field, value in validated_data.items():
            setattr(instance, field, value)

        if password:
            validate_password(password, instance)
            instance.set_password(password)

        instance.save()

        if profile_data:
            profile = instance.profile
            for field, value in profile_data.items():
                setattr(profile, field, value)
            profile.save()

        return instance
