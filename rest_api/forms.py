from django.forms import ModelForm

from gateway_backend.models import Url

class UrlForm(ModelForm):
    class Meta:
        model = Url
