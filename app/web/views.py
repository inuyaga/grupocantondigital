import conekta
from django.shortcuts import render, redirect
from app.web.models import Tipo_subcripcion
from django.urls import reverse_lazy, reverse
from django.views.generic import TemplateView, CreateView
from django.contrib.auth.views import LoginView, LogoutView
from app.web.forms import LoginForm, RegisterForm
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from app.web.models import UserPaymentCard
User = get_user_model()
conekta.api_key = 'key_7gjMqee2mr4ys93sn79TYQ'
conekta.api_version = "2.0.0"
conekta.locale = 'es'
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
        context['tipo_planes'] = Tipo_subcripcion.objects.filter(
            ts_activo=True)
        return context

class SelectCardUser(TemplateView):
    template_name = "web/select_card.html"

class SelectedSubcriptionView(LoginRequiredMixin, TemplateView):
    login_url = '/grupocanto/digital/ingresar/'
    redirect_field_name = 'redirect_to'
    template_name = "web/SelectedSub.html"

    def post(self, request, *args, **kwargs):
        conektaTokenId = request.POST.get('conektaTokenId')
        id_subcrip = kwargs['plan_id']
        type_sub = Tipo_subcripcion.objects.get(ts_id=id_subcrip)

        usercard=UserPaymentCard.objects.filter(spc_user=request.user).count()
        if usercard > 0:
            reverse_lazy('web:select_card')


        card_token=request.GET.get('card_token')
        if card_token == None:
            pass

        try:
            customer = conekta.Customer.create({
                'name': 'fulanito',
                'email': 'hdez.marioe@gmail.com',
                'phone': '9933327438',
                'metadata': {'description': 'Compra de creditos: 300(MXN)', 'reference': '1334523452345'},
                'payment_sources': [{
                    'type': 'card',
                    'token_id': conektaTokenId,
                }],
            })

            userpayment=UserPaymentCard(spc_user=request.user,spc_token_id=customer.id)
            userpayment.save()



            precio_conekta=int(type_sub.ts_precio) * 100
            orden = conekta.Order.create({
                "currency": "MXN",
                "customer_info": {
                    "customer_id": customer.id,
                },
                "line_items": [{
                    "name": type_sub.ts_nombre,
                    "unit_price": precio_conekta,
                    "quantity": 1,
                }],
                "charges": [{
                    "payment_method": {
                        "type": "default"
                    }
                }]
            })
            print(orden.id)
        except conekta.ConektaError as e:
            print(e.message)

        url = reverse_lazy('web:select_plan', kwargs={'plan_id': id_subcrip})

        return redirect(url)

        # return super().post(request, *args, **kwargs)
