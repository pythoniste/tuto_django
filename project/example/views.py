from django.contrib.auth import (
    authenticate,
    login,
    logout,
)

from django.views.generic import TemplateView
from django.urls import reverse
from django.shortcuts import render
from django.http import HttpResponseRedirect


class LoginView(TemplateView):
    """Home Page"""

    template_name = "registration/login_custom.html"

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            HttpResponseRedirect(reverse("home"))
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """
        Check auth and do the log in.
        """
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                next_uri = request.GET.get("next")
                if next_uri:
                    return HttpResponseRedirect(next_uri)
                return HttpResponseRedirect(reverse("home"))
        return HttpResponseRedirect(reverse("login"))


class LogoutView(TemplateView):
    """Home Page"""

    template_name = "registration/logout.html"

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            logout(request)
        return HttpResponseRedirect(reverse("home"))


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                next_uri = request.GET.get("next")
                if next_uri:
                    return HttpResponseRedirect(next_uri)
                return HttpResponseRedirect(reverse("home"))
        return HttpResponseRedirect(reverse("login"))
    if request.user.is_authenticated:
        HttpResponseRedirect(reverse("home"))
    context = {}
    return render(request, 'registration/login_custom.html', context)


def logout_view(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            logout(request)
        return HttpResponseRedirect(reverse("home"))
    context = {}
    return render(request, 'registration/logout.html', context)

from django.contrib.auth.decorators import login_required, permission_required