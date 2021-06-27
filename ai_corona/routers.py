from rest_framework import routers

from CT_LIS import views

default_router = routers.DefaultRouter()
default_router.register('', views.COVID19DiagnosisView)

urlpatterns = default_router.urls
