from rest_framework import serializers

from accounts.models import CustomUser, Profile


class CustomUserSerializers(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'email', 'first_name', 'last_name', 'date_joined',
                  'last_login')


class ProfileSerializers(serializers.ModelSerializer):
    user = CustomUserSerializers()

    class Meta:
        model = Profile
        fields = ('id', 'user', 'email_confirmed', 'mobile',
                  'mobile_confirmed', 'national_id', 'national_id_confirmed',
                  'medical_id', 'medical_id_confirmed')
