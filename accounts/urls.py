from django.urls import path

from rest_framework import routers

from accounts.views import CustomUserView, LogoutView

urlpatterns = [
    path('info/', CustomUserView.as_view(), name='user_info'),
    path('logout/', LogoutView.as_view(), name='user_logout'),
]
