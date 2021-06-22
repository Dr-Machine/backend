from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny

from contacts.serializers import ContactSerializer


class ContactView(CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = ContactSerializer

    def perform_create(self, serializer):
        serializer.save()
