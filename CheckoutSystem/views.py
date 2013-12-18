from django.http import HttpResponse


def index(request):
    return HttpResponse('Website under maintenance.')