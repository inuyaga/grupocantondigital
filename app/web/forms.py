from django import forms
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from app.usuario.models import User
class LoginForm(AuthenticationForm):

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('first_name','last_name','telefono','email','username')

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})


# class PagoCardForm(forms.Form):
#     name_titular=forms.CharField(max_length=100, widget=forms.TextInput(attrs={'data-conekta': 'card[name]'}))
#     def __init__(self, *args, **kwargs):
#         super(PagoCardForm, self).__init__(*args, **kwargs)
#         for field in self.fields:
#             self.fields[field].widget.attrs.update({'class': 'form-control'})
