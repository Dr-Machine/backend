from rest_framework import serializers

from accounts.serializers import CustomUserSerializers

from profiles.models import Profile


class ProfileSerializers(serializers.ModelSerializer):
    user = CustomUserSerializers()

    class Meta:
        model = Profile
        fields = [
            'id', 'user', 'email_confirmed', 'mobile', 'mobile_confirmed',
            'national_id', 'national_id_confirmed'
        ]
