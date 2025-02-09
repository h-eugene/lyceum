import django.http
from http import HTTPStatus


def home(request):
    return django.http.HttpResponse("<body>Главная</body>")


def coffee(request):
    return django.http.HttpResponse(
        "<body>Я чайник</body>", status=HTTPStatus.IM_A_TEAPOT
    )
