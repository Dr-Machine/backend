from rest_framework import routers

from CT_LIS import views

default_router = routers.DefaultRouter()

default_router.register('CT_LIS',
                        views.CTLungInfectionSegmentationSerializersView)

urlpatterns = default_router.urls
