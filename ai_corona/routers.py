from rest_framework import routers

from ai_corona import views

default_router = routers.DefaultRouter()
default_router.register('', views.COVID19DiagnosisView)

urlpatterns = default_router.urls
