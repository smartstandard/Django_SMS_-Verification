from django.shortcuts import render, redirect
from accounts.forms import PhoneNumberForm, VerificationCodeForm
from twilio.rest import Client
from django.conf import settings
import random

# Generate a random verification code
def generate_verification_code():
    return str(random.randint(100000, 999999))

def send_verification_code(request):
    if request.method == 'POST':
        form = PhoneNumberForm(request.POST)
        if form.is_valid():
            phone_number = form.cleaned_data['phone_number']
            code = generate_verification_code()

            # Send SMS via Twilio
            client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
            client.messages.create(
                body=f'Your verification code is {code}',
                from_=settings.TWILIO_PHONE_NUMBER,
                to=phone_number,
            )

            # Store the code in the session or database for verification later
            request.session['verification_code'] = code
            
            return redirect('verify_code')
    else:
        form = PhoneNumberForm()
    return render(request, 'send_code.html', {'form': form})

def verify_code(request):
    if request.method == 'POST':
        form = VerificationCodeForm(request.POST)
        if form.is_valid():
            entered_code = form.cleaned_data['code']
            if entered_code == request.session.get('verification_code'):
                # Verification successful, proceed with password reset or other actions
                return redirect('password_reset_success')
            else:
                form.add_error('code', 'Invalid verification code.')
    else:
        form = VerificationCodeForm()
    return render(request, 'verify_code.html', {'form': form})