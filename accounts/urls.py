from django.urls import path

from rest_framework import routers

from accounts.views import CustomUserView, LogoutView, ProfileView

urlpatterns = [
    path('info/', CustomUserView.as_view(), name='user_info'),
    path('logout/', LogoutView.as_view(), name='user_logout'),
]

default_router = routers.DefaultRouter()
default_router.register('profile', ProfileView)

urlpatterns += default_router.urls
