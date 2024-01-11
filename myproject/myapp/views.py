# views.py
import base64

from django.shortcuts import render, redirect
from django_otp.plugins.otp_totp.models import TOTPDevice
import qrcode
from django.contrib.auth import authenticate, login , logout
from .forms import SignupForm, LoginForm
import pyotp  # Import pyotp library for TOTP
import os
from django.conf import settings
# from django_otp.plugins.otp_totp.util import verify_token
from PIL import Image
import pyotp


# ... (your existing views)
def index(request):
    return render(request, 'index.html')





# views.py


def user_signup(request):
    qrcode_data_uri = None  # Default value
    totp_secret = pyotp.random_base32()
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()

            # Check if TOTP secret is provided and not empty
            totp_secret = pyotp.random_base32()

            if totp_secret:
                # Convert TOTP secret to hexadecimal
                totp_secret_hex = base64.b32decode(totp_secret.encode()).hex()

                # Create a TOTPDevice for the user
                totp_device = TOTPDevice(user=user, confirmed=True, key=totp_secret_hex)
                totp_device.save()

                # Generate a QR code for the TOTP secret
                qr = qrcode.QRCode(
                    version=1,
                    error_correction=qrcode.constants.ERROR_CORRECT_L,
                    box_size=10,
                    border=4,
                )
                qr.add_data(totp_secret)
                qr.make(fit=True)
                img = qr.make_image(fill_color="black", back_color="white")

                # Save the QR code image to a file
                img_path = os.path.join(settings.MEDIA_ROOT, 'qrcodes', f'{user.username}_qrcode.png')
                img.save(img_path)

                # Convert the QR code image to a data URI
                with open(img_path, "rb") as image_file:
                    qrcode_data_uri = f'data:image/png;base64,{base64.b64encode(image_file.read()).decode("utf-8")}'

            return render(request, 'signup.html', {'form': form, 'qrcode_data_uri': qrcode_data_uri,'totp_secret':totp_secret})

    else:
        form = SignupForm()

    return render(request, 'signup.html', {'form': form, 'qrcode_data_uri': qrcode_data_uri,'totp_secret':totp_secret})





def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            totp_code = form.cleaned_data['totp_code']

            user = authenticate(request, username=username, password=password)

            if user is not None:
                # Check if TOTP is enabled for the user
                totp_device = TOTPDevice.objects.filter(user=user, confirmed=True).first()
                if totp_device:
                    # TOTP is enabled, verify the TOTP code
                    if not totp_device.verify_token(totp_code):
                        # TOTP code is invalid
                        return render(request, 'login.html', {'form': form, 'error_message': 'Invalid TOTP code'})

                login(request, user)
                return redirect('home')
            else:
                # Invalid credentials
                return render(request, 'login.html', {'form': form, 'error_message': 'Invalid login details'})
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('login')