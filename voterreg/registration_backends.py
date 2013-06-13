
from django_facebook.registration_backends import FacebookRegistrationBackend
from registration_forms import RegistrationFormWithCaptcha

class VoterregRegistrationBackend(FacebookRegistrationBackend):
    def get_form_class(self, request):
        return RegistrationFormWithCaptcha
