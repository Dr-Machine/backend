from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/auth/', include('djoser.urls')),
    path('api/auth/', include('djoser.urls.jwt')),

    path('api/accounts/', include('accounts.urls')),

    path('api/contacts/', include('contacts.urls')),

    path('api/services/CT_LIS/', include('CT_LIS.routers')),
    path('api/services/CT_LIS/', include('CT_LIS.routers')),

    path('api/profiles/', include('profiles.routers')),
]
