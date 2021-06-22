from django.urls import path

from contacts.views import ContactView

urlpatterns = [
    path('', ContactView.as_view(), name='contact'),
]
