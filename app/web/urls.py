from django.urls import path
from app.web import views as WebView
app_name = "web"
urlpatterns = [
    path('', WebView.IndexView.as_view(), name="inicio"),
    path('grupocanton/digital/ingresar/', WebView.IngrsarView.as_view(), name="login"), 
    path('grupocanton/digital/salir/', WebView.SalirView.as_view(), name="logout"),
    path('grupocanton/digital/registar/', WebView.RegisterUserView.as_view(), name="registro"),
    path('grupocanton/planes/', WebView.PlanesView.as_view(), name="planes"),

    path('grupocanton/planes/<int:plan_id>/', WebView.SelectTipoPago.as_view(), name="select_tip_pago"),
    path('grupocanton/planes/selected/<int:plan_id>/metodo-<slug:method>/', WebView.PagoSubcripcionView.as_view(), name="pago"),
    # path('grupocanton/planes/selected/<int:plan_id>/metodo-<slug:method>/', WebView.PagoSubcripcionView.as_view(), name="pago"),
    path('grupocanton/conekta/web-hock/notifications/request', WebView.WebhooksConekta.as_view(), name="conekta_webhooks"),
    path('grupocanton/referencias/', WebView.CargoUserList.as_view(), name="referencias"),
    path('grupocanton/referencias/oxxo/<slug:ord>/', WebView.ReferenciaOxxoViewPdf.as_view(), name="referencia_pdf"),


    path('grupocanto/digital/prensa/', WebView.PrensaDigitalView.as_view(), name="ediciones"),
    path('grupocanto/digital/prensa/paper-read/slug-reder-1212<int:pk>98765-info-canton/', WebView.ReaderNew.as_view(), name="reder_paper"),
]