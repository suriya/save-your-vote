
from django import forms
from captcha.fields import ReCaptchaField
from django_facebook.forms import FacebookRegistrationFormUniqueEmail

class FormWithCaptcha(forms.Form):
    pass
#     captcha = ReCaptchaField()

class RegistrationFormWithCaptcha(FacebookRegistrationFormUniqueEmail, FormWithCaptcha):
    pass
