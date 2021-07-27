from __future__ import absolute_import
from django.urls import reverse_lazy
from register.models import *
from django.shortcuts import get_object_or_404, render, redirect
from register.forms import ClientRegisterForm, SpecialistRegisterForm, LoginForm
from users.decorators import client_required, specialist_required
from django.views import generic
from braces.views import AnonymousRequiredMixin, FormValidMessageMixin, LoginRequiredMixin, MessageMixin
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.db import transaction
from main.views import HomePageView
from django.conf import settings


def register(request):
    return render(request, 'register.html')

class ClientRegistration(AnonymousRequiredMixin, FormValidMessageMixin, generic.CreateView):
    form_class = ClientRegisterForm
    model = User
    template_name = 'client_register.html'
    authenticated_redirect_url = settings.LOGIN_URL
#   success_url = settings.LOGIN_URL

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'client'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        messages.success(self.request, 'Account was created for ' + user)
        return redirect('registration:login')

class SpecialistRegistration(AnonymousRequiredMixin, FormValidMessageMixin, generic.CreateView):
    form_class = SpecialistRegisterForm
    model = Specialist
    template_name = 'specialist_register.html'
    authenticated_redirect_url = settings.LOGIN_URL
    #success_url = settings.LOGIN_URL

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'specialist'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        messages.success(self.request, 'Account was created for ' + user)
        return redirect('registration:login')



class LoginView(AnonymousRequiredMixin, FormValidMessageMixin, generic.FormView):
    form_class = LoginForm
    authenticated_redirect_url = "/accounts/<int:id>/"
    form_valid_message = _(u"You are successfully logged in!")
    template_name = 'login2.html'

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(username=username, password=password)

        if user is not None and user.is_active:
            messages.success(self.request, user + 'You are successfully logged in!')
            login(self.request, user)
            return super(LoginView, self).form_valid(form)
        else:
            messages.error(self.request, "Unsuccessful registration. Invalid information.")
            return self.form_invalid(form)


class LogOutView(LoginRequiredMixin, MessageMixin, generic.RedirectView):
    url = redirect('phoenix/home')

    def get(self, request, *args, **kwargs):
        logout(request)
        messages.success("You've been logged out. Come back soon!")
        return super(LogOutView, self).get(request, *args, **kwargs)


class PasswordReset():
    pass

class PasswordChange():
    pass