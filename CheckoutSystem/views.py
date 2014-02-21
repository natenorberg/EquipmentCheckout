from django.contrib.auth import logout
from django.contrib.auth.views import password_reset
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, render
from django.template import RequestContext


def custom_400_view(request):
    return render_to_response("custom_400.html", context_instance=RequestContext(request))


def custom_403_view(request):
    return render_to_response("custom_403.html", context_instance=RequestContext(request))


def custom_404_view(request):
    return render_to_response("custom_404.html", context_instance=RequestContext(request))


def custom_500_view(request):
    return render_to_response("custom_500.html", context_instance=RequestContext(request))


def index(request):
    return render_to_response("welcome.html", context_instance=RequestContext(request))


@login_required
def progress(request):
    return render_to_response("progress.html", context_instance=RequestContext(request))


def reset_password(request):
    if request.method == 'POST':
        return password_reset(request,
            from_email=request.POST.get('email'))
    else:
        return render(request, 'reset_password.html')


def logout_view(request):
    logout(request)
    return HttpResponseRedirect("/welcome/")