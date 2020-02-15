from django.urls import path
from app.web import views as WebView
app_name = "web"
urlpatterns = [
    path('', WebView.IndexView.as_view(), name="inicio"),
    path('grupocanto/digital/ingresar/', WebView.IngrsarView.as_view(), name="login"),
    path('grupocanto/digital/salir/', WebView.SalirView.as_view(), name="logout"),
    path('grupocanto/digital/registar/', WebView.RegisterUserView.as_view(), name="registro"),
    path('grupocanto/planes/', WebView.PlanesView.as_view(), name="planes"),
]