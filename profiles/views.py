from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated

from profiles.models import Profile
from profiles.serializers import ProfileSerializers


class ProfileView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
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
