from rest_framework import routers

from profiles import views

default_router = routers.DefaultRouter()

default_router.register('', views.ProfileView)

urlpatterns = default_router.urls
