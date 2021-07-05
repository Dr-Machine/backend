import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

application = get_wsgi_application()

with open('ascii.txt', 'r') as f:
    ascii_logo = f.read()
    print(ascii_logo)
