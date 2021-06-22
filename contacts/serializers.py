from rest_framework import serializers

from contacts.models import Contact


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = [
            'id', 'email', 'first_name', 'last_name', 'subject', 'message'
        ]

    def create(self, validate_data):
        instance = super(ContactSerializer, self).create(validate_data)
        return instance
