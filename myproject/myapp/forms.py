


# forms.py



from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class SignupForm(UserCreationForm):
    totp_secret = forms.CharField(
        required=False,
        widget=forms.HiddenInput(),
        help_text="Scan this QR code with your TOTP app to enable two-factor authentication."
    )

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'totp_secret']

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    totp_code = forms.CharField(
        required=False,
        help_text="Enter the code from your TOTP app.",
        widget=forms.TextInput(attrs={'autocomplete': 'off'})
    )

