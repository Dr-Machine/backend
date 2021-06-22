# Backend for Dr. Machine

This application is developed using:
- [Django](https://www.djangoproject.com/) - [Django REST Framework](https://www.django-rest-framework.org/) - [Djoser](https://djoser.readthedocs.io/en/latest/getting_started.html)
- [Celery](https://docs.celeryproject.org/en/stable/) - [Redis](https://redis.io/)
- [Keras](https://keras.io/) - [PyDicom](https://pydicom.github.io/)
- [lungmask](https://github.com/JoHof/lungmask) package (utilizing [PyTorch](https://pytorch.org/))

## Usage
- Create a virtual environment:
    ```shell
    $ python -m venv .venv
    ```
- Activate the virtual environment:
    ```shell
    $ source .venv/bin/activate
    ```
- Install the required packages:
    ```shell
    $ pip install -r requirements.txt
    ```
- Apply Django migrations:
    ```shell
    $ python manage.py migrate
    ```
- Create a super-user:
    ```shell
    $ python manage.py createsuperuser
    ```
- Start the Redis worker (make sure you have Redis installed):
    ```shell
    $ celery -A backend.celery worker --pool=solo -l info
    ```
- In a seperate terminal, run server:
    ```shell
    $ python manage.py runserver --settings=backend.settings.development
    ```