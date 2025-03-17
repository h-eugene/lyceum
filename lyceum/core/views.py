from http import HTTPStatus

import django.http


def coffee(request):
    return django.http.HttpResponse("Я чайник", status=HTTPStatus.IM_A_TEAPOT)


__all__ = ["coffee"]
