import django.http
import django.shortcuts


def home(request):
    template = "homepage/main.html"
    return django.shortcuts.render(request, template)
