from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext


def index(request):
    return render_to_response("welcome.html", context_instance=RequestContext(request))


@login_required
def progress(request):
    return render_to_response("progress.html", context_instance=RequestContext(request))


def logout_view(request):
    logout(request)
    return HttpResponseRedirect("/welcome/")