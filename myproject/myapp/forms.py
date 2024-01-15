

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
        labels = {
            'username': '',
            'password1': '',
            'password2': '',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs['autocomplete'] = 'new-password'
        self.fields['password2'].widget.attrs['autocomplete'] = 'new-password'

        self.fields['username'].widget.attrs.update({
            'class': 'block w-full p-2 text-center bg-transparent shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-md',
            'placeholder': 'Username',
            'aria-label': 'Username',
            'data-tooltip-content': 'Required 150 characters or fewer.<br>Letters, digits and @/./+/-/_ only.'
        })
        self.fields['password1'].widget.attrs.update({
            'class': 'block w-full p-2 text-center bg-transparent shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-md',
            'placeholder': 'Password',
            'aria-label': 'Password',
            'data-tooltip-content': 'Your password should not be too similar to your other personal information.<br>Your password must contain at least 8 characters.<br>Your password cannot be a commonly used password.<br>Your password cannot be entirely numeric.'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'block w-full p-2 text-center bg-transparent shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-md',
            'placeholder': 'Confirm Password',
            'aria-label': 'Confirm Password',
            'data-tooltip-content': 'Enter the same password as before'
        })
        self.fields['totp_secret'].widget.attrs.update({
            'class': 'hidden',
            'data-tooltip-content': 'Scan this QR code with your TOTP app to enable two-factor authentication.'
        })
        self.fields['username'].help_text = ''
        self.fields['username'].widget.attrs['onclick'] = "this.setAttribute('data-tooltip-content', 'Required 150 characters or fewer.<br>Letters, digits and @/./+/-/_ only.')"
        self.fields['password1'].label = ''
        self.fields['password1'].help_text = ''
        self.fields['password2'].help_text = ''
        self.fields['password2'].label = ''



class LoginForm(forms.Form):
    username = forms.CharField(
       label='',
       widget=forms.TextInput(attrs={
        'class': 'block w-full p-2 text-center bg-transparent shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-md',
        'placeholder': 'Username',
        'aria-label': 'Username'
    }))
    password = forms.CharField(
        label='', 
        widget=forms.PasswordInput(attrs={
            'class': 'block w-full p-2 text-center bg-transparent shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-md',
            'placeholder': 'Password',
            'aria-label': 'Password'
        }))
    totp_code = forms.CharField(
        required=False,
        label='', 
        widget=forms.TextInput(attrs={
            'class': 'block w-full p-2 text-center bg-transparent shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-md',
            'placeholder': 'TOTP Code',
            'aria-label': 'TOTP Code',
            'title': "Enter the code from your TOTP app.",
            'data-target': 'totp-help-text',
            'data-tooltip-content': ".tooltip"
        }))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['totp_code'].widget.attrs['autocomplete'] = 'off'

        


