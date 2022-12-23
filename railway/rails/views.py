from django.shortcuts import redirect, render
from django.views.generic.base import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, FormView
from django.views.generic.edit import FormMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.contrib.auth import login, authenticate, logout
from django.core.cache import cache
from django.http import JsonResponse, HttpResponseRedirect
from django.views.decorators.cache import cache_page

from .utlis import DataMixin
from user.models import User
from .models import *
from .forms import *

def page_not_found_view(request, exception):
    return render(request, '404.html', status=404)

class MainView(DataMixin, ListView):
    model = City
    template_name = 'index.html'

    def get_context_data(self, *, object_list = None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(form=MainForm())
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        return City.objects.all()

class TrainsView(DataMixin, ListView):
    model = Train
    template_name = 'railway/trains_list.html'
    context_object_name = 'trains_list'

    def get_context_data(self, *, object_list = None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context()
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        data = self.request.GET
        start_city = data.get('start_city')
        end_city = data.get('end_city')
        start_date = data.get('start_date')
        return Train.objects.filter(start_city=start_city, end_city=end_city, start_date=start_date).order_by('start_time')

class TrainDetailView(DataMixin, DetailView):
    model = Train
    template_name = 'railway/train.html'
    context_object_name = 'train'

    def get_context_data(self, *, object_list = None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context()
        return dict(list(context.items()) + list(c_def.items()))


class BuyTicket(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        form = BuyForm(request.POST)
        if form.is_valid():
            print(form.data)
            form.save()
            return redirect('index')


class ProfileView(DataMixin, FormView):
    # model = User
    form_class = ProfileForm
    template_name = 'railway/profile.html'
    context_object_name = 'user'
    succes_url = reverse_lazy('profile')

    def get_context_data(self, *, object_list = None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context()
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        print(form)
        return redirect('profile')

class RegView(DataMixin, CreateView):
    form_class = RegForm
    template_name = 'railway/registration.html'
    success_url = reverse_lazy('index')

    def get_context_data(self, *, object_list = None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context()
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        email = form.save()
        login(self.request, email)
        return redirect('index')

class LoginView( DataMixin, LoginView):
    form_class = LoginForm
    template_name = 'railway/login.html'

    def get_context_data(self, *, object_list = None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context()
        return dict(list(context.items()) + list(c_def.items()))

    def get_success_url(self):
        return reverse_lazy('index')

def logout_user(request):
    logout(request)
    return redirect('login')


