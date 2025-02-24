import django.http
import django.shortcuts


def home(request):
    return django.http.HttpResponse("<body>Главная</body>")


def index_render(request):
    template = "homepage/home.html"
    return django.shortcuts.render(request, template)
