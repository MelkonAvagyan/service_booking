from django.shortcuts import get_object_or_404, render, redirect

from __future__ import absolute_import
from users.models import *
from users.forms import *
from django.views import generic
from braces.views import AnonymousRequiredMixin, FormValidMessageMixin, LoginRequiredMixin, MessageMixin
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from users.decorators import client_required, specialist_required
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse_lazy
from django.conf import Settings


#shows specialists per category
class SpecialistsList(generic.ListView):
    template = 'specialists.html'
    queryset = SpecialistProfile.objects.all().order_by('reviews') #filter by category

#clients of specific specialist
class ClientsList(generic.ListView):
    template = 'clients.html'
    queryset = ClientProfile.objects.all().order_by('date_created')


#profiel look-up for client
class SpecialistDetail(generic.DetailView):
    template_name = 'specialist.html'

    def get_object(self, id):
        id_ = self.kwargs.get('id')
        return get_object_or_404(SpecialistProfile, id_=id)

#same for client
class ClientDetail(generic.DetailView):
    template_name = 'client.html'

    def get_object(self, id):
        id_ = self.kwargs.get('id')
        return get_object_or_404(ClientProfile, id_=id)

#personal profile of specialist
class SpecialistProfile(generic.CreateView):
    def get(self, request, *args, **kwargs):
        context = {'form': SpecialistProfileForm()}
        return render(request, 'specialist.html', context)

#... of client
class ClientProfile(generic.CreateView):
    def get(self, request, *args, **kwargs):
        context = {'form': ClientProfileForm()}
        return render(request, 'specialist.html', context)


class Reviews(generic.ListView):
    template = 'reviews.html'
    queryset = Reviews.objects.all().order_by('updated at')

#chat btw user and specialist
def createMessage(request, pk):
    recipient = Specialist.objects.get(id=pk)
    form = MessageForm()

    try:
        sender = request.user.profile
    except:
        sender = None

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = sender
            message.recipient = recipient

            if sender:
                message.name = sender.name
                message.email = sender.email
            message.save()

            messages.success(request, 'Your message was successfully sent!')
            return redirect('user-profile', pk=recipient.id)

    context = {'recipient': recipient, 'form': form}
    return render(request, 'users/message_form.html', context)