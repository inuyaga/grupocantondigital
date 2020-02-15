from django.shortcuts import render
from app.web.models import Tipo_subcripcion
from django.urls import reverse_lazy, reverse
from django.views.generic import TemplateView, CreateView
from django.contrib.auth.views import LoginView, LogoutView
from app.web.forms import LoginForm, RegisterForm
from django.contrib.auth import get_user_model
User = get_user_model()

# Create your views here.

class IndexView(TemplateView):
    template_name = "web/inicio.html"

class IngrsarView(LoginView): 
    template_name = "ingresar.html"
    form_class = LoginForm

class SalirView(LogoutView): 
    template_name = "salir.html"

class RegisterUserView(CreateView): 
    model = User
    template_name = "registrar.html"
    form_class = RegisterForm
    success_url = reverse_lazy('web:login')

class PlanesView(TemplateView):
    template_name = "web/planes.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tipo_planes'] = Tipo_subcripcion.objects.filter(ts_activo=True)
        return context