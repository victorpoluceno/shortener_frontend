import json
import urllib

from django.test import TestCase
from django.test.client import Client

from django.contrib.auth.models import User

from rest_api.api import UrlThrottle


class ApiTest(TestCase):
    def test_url_throttle(self):
        from django.conf import settings
        settings.SHOULD_BE_THROTTLE = False

        url_throttle = UrlThrottle()
        self.assertEqual(url_throttle.should_be_throttled('x'), False)
