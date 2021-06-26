from django.urls import path

from CT_LIS.views import CTLungInfectionSegmentationSerializersView

urlpatterns = [
    path('',
         CTLungInfectionSegmentationSerializersView.as_view(),
         name='CT_LIS'),
]
