
import re
from django.db.models import CharField
from django.core.validators import RegexValidator
from django import forms

epic_re = re.compile(r'^[A-Z]{3}\d{7}|[A-Z]{2}/\d{2}/\d{3}/\d{7}', re.IGNORECASE)
validate_epic = RegexValidator(epic_re, 'Enter a valid Voter ID number, example: ABC1234567, or UP/01/234/1234567', 'invalid')

class EPICNumberFormField(forms.CharField):
    default_error_messages = {
        'invalid': 'Enter a valid Voter ID number, example: ABC1234567, or UP/01/234/1234567',
    }
    default_validators = [ validate_epic ]

class EPICNumberField(CharField):
    description = "Voter ID Number"

    def __init__(self, verbose_name=None, name=None, **kwargs):
        kwargs['max_length'] = kwargs.get('max_length', 200)
        CharField.__init__(self, verbose_name, name, **kwargs)
        self.validators.append(validate_epic)

    def formfield(self, **kwargs):
        # As with CharField, this will cause URL validation to be performed
        # twice.
        defaults = {
            'form_class': EPICNumberFormField,
        }
        defaults.update(kwargs)
        return super(EPICNumberField, self).formfield(**defaults)
