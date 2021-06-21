from django.utils import timezone

from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.models import Profile
from accounts.serializers import CustomUserSerializers, ProfileSerializers


class CustomUserView(APIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = CustomUserSerializers

    def get(self, request, format=None):
        return Response(data=self.serializer_class(request.user).data,
                        status=status.HTTP_200_OK)


class LogoutView(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request, format=None):
        user = request.user
        user.last_login = timezone.now()
        user.save()
        data = {"message": "User logged out successfully!"}
        return Response(data=data, status=status.HTTP_200_OK)


class ProfileView(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, )
    queryset = Profile.objects.all()
    lookup_field = 'id'
    lookup_url_kwarg = 'id'

    def get_serializer_class(self):
        return ProfileSerializers

    def filter_queryset(self, queryset):
        queryset = self.get_queryset().filter(user=self.request.user)
        return queryset

    def list(self, request, *args, **kwargs):
        self.kwargs['id'] = request.user.profile.id
        return self.retrieve(request, *args, **kwargs)
