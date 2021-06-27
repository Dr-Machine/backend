from rest_framework import routers

from CT_LIS import views

default_router = routers.DefaultRouter()
default_router.register('', views.CTLungInfectionSegmentationView)

urlpatterns = default_router.urls
