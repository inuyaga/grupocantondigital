from django.urls import path
from app.web import views as WebView

app_name = "web"
urlpatterns = [
    path('', WebView.IndexView.as_view(), name="inicio"),
]