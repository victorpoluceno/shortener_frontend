from django.db import models

from tastypie.resources import ModelResource
from tastypie.authentication import ApiKeyAuthentication
from tastypie.authorization import DjangoAuthorization
from tastypie.throttle import CacheThrottle
from tastypie.validation import FormValidation

from gateway_backend.tasks import url_short
from gateway_backend.models import Url

from rest_api.forms import UrlForm

from django.conf import settings


class UrlThrottle(CacheThrottle):
    def should_be_throttled(self, identifier, **kwargs):
        try:
            should_be_throttled = settings.SHOULD_BE_THROTTLED
        except (AttributeError):
            should_be_throttled = True

        if super(UrlThrottle, self).should_be_throttled(identifier, **kwargs) \
                and should_be_throttled:
            return True

        return False


class UrlResource(ModelResource):
    class Meta:
        resource_name = 'url'
        queryset = Url.objects.all()
        fields = ['long_url', 'key']
        authentication = ApiKeyAuthentication()
        authorization = DjangoAuthorization()
        throttle = UrlThrottle(throttle_at=100)
        allowed_methods = ['get', 'post']
        validation = FormValidation(form_class=UrlForm)


def url_post_save(sender, **kwargs):
    instance = kwargs.get('instance')
    if kwargs.get('created') == True:
        url_short.delay(instance.id)

models.signals.post_save.connect(url_post_save, sender=Url, 
        dispatch_uid='url_create')
