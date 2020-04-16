from django.urls import reverse_lazy
import os
import conekta
from django.shortcuts import render, redirect
from app.web.models import Tipo_subcripcion, Orden, Edicion, Subscription, Diario
from django.urls import reverse_lazy, reverse
from django.views.generic import TemplateView, CreateView, View, ListView, DetailView
from django.contrib.auth.views import LoginView, LogoutView
from app.web.forms import LoginForm, RegisterForm
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from django.contrib.humanize.templatetags.humanize import intcomma

# formateo de zona horaria display
from django.utils.formats import localize
from datetime import datetime, timedelta

# Librerias reportlab a usar:
from django.http import HttpResponse
from io import BytesIO
from django.conf import settings
from reportlab.platypus import (SimpleDocTemplate, PageBreak, Image, Spacer,
                                Paragraph, Table, TableStyle, Spacer, BaseDocTemplate, Frame, PageTemplate)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import A4, letter, landscape
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER, TA_RIGHT, TA_LEFT
PAGE_WIDTH = letter[0]
PAGE_HEIGHT = letter[1]


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
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

    def form_valid(self, form):
        self.object = form.save()
        # self.object.first_name=form.instance.first_name
        # self.object.last_name=form.instance.last_name
        # self.object.email=form.instance.email
        form.instance.first_name = form.cleaned_data['first_name']
        form.instance.last_name = form.cleaned_data['last_name']
        form.instance.email = form.cleaned_data['email']
        return super().form_valid(form)


class PlanesView(TemplateView):
    template_name = "web/planes.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tipo_planes'] = Tipo_subcripcion.objects.filter(
            ts_activo=True)
        return context


class SelectTipoPago(LoginRequiredMixin, TemplateView):
    login_url = '/grupocanto/digital/ingresar/'
    redirect_field_name = 'redirect_to'
    template_name = "web/select_method_pay.html"


class PagoSubcripcionView(LoginRequiredMixin, TemplateView):
    login_url = '/grupocanto/digital/ingresar/'
    redirect_field_name = 'redirect_to'
    template_name = "web/pago_sub.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tipo_sub'] = Tipo_subcripcion.objects.get(
            ts_id=self.kwargs['plan_id'])

        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        # customer = conekta.Customer.find("cus_2nDBvXTnPV3y8wAfR")
        # data = customer['payment_sources'][0]
        # print(data['type'])
        # order = conekta.Order.find("ord_2fw8EWJusiRrxdPzT")

        order = conekta.Order.find("ord_2nGW3ox46D5x3e8sR")
        print(order.charges[0])
        print(order.charges[0].payment_method.barcode_url)
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        from datetime import datetime, timedelta
        from django.utils.timezone import make_aware
        url = reverse_lazy('web:ediciones')

        conektaTokenId = request.POST.get('conektaTokenId')
        spc_payment_source_id = request.POST.get('spc_payment_source_id')
        id_subcrip = kwargs['plan_id']
        type_sub = Tipo_subcripcion.objects.get(ts_id=id_subcrip)
        customer_id = ""
        UserPaymentID = 0
        ahora = datetime.utcnow()
        nex2_days = ahora + timedelta(days=2)
        timestamp = datetime.timestamp(nex2_days)

        if self.kwargs.get('method') == 'oxxo':
            try:
                precio_conekta = type_sub.ts_precio * 100
                data = {
                    "line_items": [
                        {
                            "name": type_sub.ts_nombre,
                            "description": type_sub.ts_descripcion,
                            "unit_price": int(precio_conekta),
                            "quantity": 1,
                            "category": "Servicios digitales",
                            "type": "digital",
                            "tags": ["periodico", "tabasco hoy", 'imprenta digital', 'tabasco']
                        }
                    ],
                    "customer_info": {
                        "name": request.user.get_full_name(),
                        "phone": request.user.telefono,
                        "email": request.user.email,
                        "corporate": False,
                        "vertical_info": {}
                    },
                    "charges": [{
                        "payment_method": {
                            "type": "oxxo_cash",
                            'expires_at': int(timestamp)
                        },
                        "amount": int(precio_conekta)
                    }],
                    "currency": "mxn",
                    "metadata": {"test": "extra info"}
                }

                order = conekta.Order.create(data)
                # temp = datetime.fromtimestamp(order.charges[0].payment_method.expires_at)

                # vigencia = timezone.make_aware(temp)
                datetime_obj_with_tz = make_aware(datetime.fromtimestamp(order.charges[0].payment_method.expires_at))
                odr = Orden(
                    ord_user=request.user,
                    ord_tipo_sub_id=type_sub.ts_id,
                    ord_payment_status=order.payment_status,
                    ord_monto=type_sub.ts_precio,
                    ord_order_id=order.id,
                    ord_charger_id=order.charges[0].id,
                    ord_referencia=order.charges[0].payment_method.reference,
                    ord_expira_en=datetime_obj_with_tz,
                    ord_type_cargo=order.charges[0].payment_method.type,
                    ord_barcode_url=order.charges[0].payment_method.barcode_url
                )
                odr.save()
                sub = Subscription(
                    sub_orden=odr,
                    sub_inicial=datetime.now(),
                    sub_final=datetime.now() + timedelta(days=type_sub.ts_tiempo)
                )
                sub.save()
                url = reverse_lazy('web:referencia_pdf', kwargs={'ord': odr.ord_order_id})
                # return redirect(url)
            except conekta.ConektaError as e:
                messages.warning(self.request, e.message)

        elif self.kwargs.get('method') == 'card':
            print('soy tarjeta')

            try:
                if conektaTokenId != None:
                    customer = conekta.Customer.create({
                        'name': str(request.user.get_full_name()),
                        'email': request.user.email,
                        'phone': request.user.telefono,
                        'metadata': {'description': type_sub.ts_descripcion, 'reference': type_sub.ts_nombre},
                        'payment_sources': [{
                            'type': 'card',
                            'token_id': conektaTokenId,
                        }],
                    })

                    precio_conekta = int(type_sub.ts_precio) * 100
                    orden = conekta.Order.create({
                        "currency": "MXN",
                        "customer_info": {
                            "customer_id": customer.id,
                        },
                        "line_items": [{
                            "name": "Subcripcion {}".format(type_sub.ts_nombre),
                            "unit_price": precio_conekta,
                            "quantity": 1,
                        }],
                        "charges": [{
                            "payment_method": {
                                "type": "default"
                            }
                        }]
                    })
                    
                    odr = Orden(
                        ord_user=request.user,
                        ord_tipo_sub_id=type_sub.ts_id,
                        ord_payment_status=orden.payment_status,
                        ord_monto=type_sub.ts_precio,
                        ord_order_id=orden.id,
                        ord_charger_id=orden.charges[0].id,
                        ord_referencia=orden.charges[0].payment_method.last4,
                        ord_expira_en=datetime.now(),
                        ord_type_cargo=orden.charges[0].payment_method.type,
                        ord_barcode_url=orden.charges[0].payment_method.object
                    )
                    odr.save()
                    sub = Subscription(
                        sub_orden=odr,
                        sub_inicial=datetime.now(),
                        sub_final=datetime.now() + timedelta(days=type_sub.ts_tiempo),
                        sub_status=True
                    )
                    sub.save()
                    url = reverse_lazy('web:ediciones')

            except conekta.ConektaError as e:
                messages.warning(self.request, e.message)

        # url = reverse_lazy('web:select_plan', kwargs={'plan_id': id_subcrip})

        return redirect(url)

        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)


@method_decorator(csrf_exempt, name='dispatch')
class WebhooksConekta(TemplateView):
    template_name = "webhooks.html"

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        print('he recibido respuesta de webhock')
        print(request)
        return self.render_to_response(context)


class CargoUserList(ListView):
    template_name = "user/cargo_user.html"
    model = Orden

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(
            ord_user=self.request.user, ord_payment_status='pending_payment', ord_type_cargo='oxxo')
        print(queryset)
        return queryset


class ReferenciaOxxoViewPdf(View):

    # def dispatch(self, *args, **kwargs):

    #     return super().dispatch(*args, **kwargs)

    def myFirstPage(self, canvas, doc):

        # CABECERA DE PAGINA
        Title = "FICHA DIGITAL NO ES NECESARIO IMPRIMIR"
        canvas.saveState()
        canvas.setFont('Times-Bold', 16)

        canvas.drawCentredString(PAGE_WIDTH/2.0, PAGE_HEIGHT - 50, Title)
        # Logo de empresa
        # archivo_imagen = self.object_catalogo.tp_empresa.empresa_logo.path
        # Definimos el tamaño de la imagen a cargar y las coordenadas correspondientes
        # canvas.drawImage(archivo_imagen, 20, 690, 120, 90, preserveAspectRatio=True)

        canvas.saveState()
        canvas.setFont('Times-Roman', 10)

        canvas.drawString(420, 30, '{}'.format(localize(datetime.now())))

    def myLaterPages(self, canvas, doc):
        canvas.saveState()
        canvas.setFont('Times-Roman', 10)
        canvas.drawString(420, 30, '{}'.format(localize(datetime.now())))
        canvas.restoreState()

    def get(self, request, *args, **kwargs):
        response = HttpResponse(content_type='application/pdf')
        buff = BytesIO()
        doc = SimpleDocTemplate(buff, pagesize=letter, rightMargin=40, leftMargin=40,
                                topMargin=60, bottomMargin=30, title='REFERENCIA OXXO')
        items = []

        stylo_p_center = ParagraphStyle(
            'parrafo_center', alignment=TA_CENTER, fontSize=11, fontName="Times-Roman")
        stylo_p_derecha = ParagraphStyle(
            'parrafo_center', alignment=TA_RIGHT, fontSize=11, fontName="Times-Roman")
        stylo_p_izquierda = ParagraphStyle(
            'parrafo_center', alignment=TA_LEFT, fontSize=12, fontName="Times-Roman")
        stylo_p_center_INFO = ParagraphStyle(
            'parrafo_center', alignment=TA_CENTER, fontSize=8, fontName="Times-Roman")
        stylo_p = ParagraphStyle(
            'parrafo', alignment=TA_LEFT, fontSize=18, fontName="Times-Roman")
        stylo_titulo = ParagraphStyle(
            'titulo', alignment=TA_CENTER, fontSize=14, fontName="Times-Bold")
        stylo_titulo_normal = ParagraphStyle(
            'titulo', alignment=TA_CENTER, fontSize=14, fontName="Times-Roman")
        stylo_portada_title = ParagraphStyle(
            'titulo', alignment=TA_CENTER, fontSize=20, fontName="Times-Bold")

        ord_object = Orden.objects.get(ord_order_id=self.kwargs['ord'])

        dta = []

        items.append(Image(os.path.realpath(
            'static/img/oxxopay1.jpg'), 8*cm, 5*cm))
        text = """MONTO A PAGAR"""
        items.append(Paragraph(text, stylo_titulo))
        items.append(Spacer(0, 10))

        text = """${} MXN""".format(intcomma(ord_object.ord_monto))
        items.append(Paragraph(text, stylo_titulo_normal))
        items.append(Spacer(0, 10))

        text = """OXXO Cobra una comision al momento de realizar el pago"""
        items.append(Paragraph(text, stylo_titulo_normal))
        items.append(Spacer(0, 20))

        text = """REFERENCIA"""
        items.append(Paragraph(text, stylo_p))
        items.append(Spacer(0, 20))

        text = """{}""".format(ord_object.ord_referencia)
        items.append(Paragraph(text, stylo_portada_title))
        items.append(Spacer(0, 15))
        items.append(Image(ord_object.ord_barcode_url, 5*cm, 1.5*cm))
        items.append(Spacer(0, 30))

        text = """INSTRUCCIONES"""
        items.append(Paragraph(text, stylo_titulo))
        items.append(Spacer(0, 20))

        text = """1. Acude a la tienda OXXO más cercana."""
        items.append(Paragraph(text, stylo_p_izquierda))
        items.append(Spacer(0, 10))

        text = """2. Indica en caja que quieres realizar un pago de OXXOPay"""
        items.append(Paragraph(text, stylo_p_izquierda))
        items.append(Spacer(0, 10))

        text = """3. Dicta al cajero el número de referencia en esta ficha para que tecleé directamente en la pantalla de venta."""
        items.append(Paragraph(text, stylo_p_izquierda))
        items.append(Spacer(0, 10))

        text = """4. Realiza el pago correspondiente con dinero en efectivo."""
        items.append(Paragraph(text, stylo_p_izquierda))
        items.append(Spacer(0, 10))

        text = """5. Al confirmar tu pago, el cajero te entregará un comprobante impreso. En el podrás verificar que se haya realizado correctamente.Conserve este comprobante de pago."""
        items.append(Paragraph(text, stylo_p_izquierda))
        items.append(Spacer(0, 10))

        # data_table = [(
        #     Image(os.path.realpath('static/img/OXXO.png'), 5*cm, 5*cm),
        #     Paragraph(text, stylo_p),
        #     )]

        # tabla = Table(data_table, colWidths=[
        #     15 * cm,
        #     5 * cm,
        #     ])

        # tabla.setStyle(TableStyle(
        #     [
        #         ('GRID', (0, 0), (-1, -1), 1, colors.black),
        #         # ('LINEBELOW', (0, 0), (-1, 0), 0, colors.darkblue),
        #         ('BACKGROUND', (0, 0), (-1, 0), colors.transparent)
        #     ]
        # ))

        # items.append(tabla)

        # items.append(Paragraph("FICHA DIGITAL NOES NECESARIO IMPRIMIR", stylo_titulo))

        # items.append(Spacer(0, 20))

        doc.build(items, onFirstPage=self.myFirstPage,
                  onLaterPages=self.myLaterPages)
        response.write(buff.getvalue())
        buff.close()
        return response


class PrensaDigitalView(ListView):
    model = Edicion
    template_name = "web/prensadigital.html"
    def get_queryset(self):

        queryset = super().get_queryset()
        ahora = datetime.now()
        date_init = datetime(ahora.year, ahora.month, ahora.day, 00, 00, 00, 00000)
        queryset = queryset.filter(ed_fecha_publicacion__range=[date_init, ahora]).order_by('ed_fecha_publicacion')
        print(ahora)
        return queryset


class ReaderNew(DetailView): 
    model = Edicion
    template_name = "web/read_new.html"

    
    def dispatch(self, request, *args, **kwargs):

        ordn=Orden.objects.filter(
            ord_user=self.request.user, 
            ord_type_cargo='oxxo',
            ord_expira_en__gte=datetime.now(),
            ).order_by('-ord_id')
        for target_list in ordn:
            order = conekta.Order.find(target_list.ord_order_id)
            print(order.charges[0].payment_method.barcode_url)

        

        return super(ReaderNew, self).dispatch(request, *args, **kwargs)

    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['info']=Subscription.objects.filter(sub_status=True, sub_final__gte=datetime.now(), sub_orden__ord_user=self.request.user)
        return context
    
    
class MiCuentaView(TemplateView):
    template_name = "web/micuenta.html" 