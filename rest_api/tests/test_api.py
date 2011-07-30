import json
import urllib

from django.test import TestCase
from django.test.client import Client

from django.contrib.auth.models import User


class SmokeTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.base_url = '/api/v1/url/'

        self.user = User.objects.create_user('tests', \
                email='victorpoluceno@gmail.com')
        self.user.is_superuser = True
        self.user.is_staff = True
        self.user.save()

    def test_url_short_api(self):
        auth_chunk = urllib.urlencode([('username', self.user.username), 
                ('api_key', self.user.api_key.key)])

        url = ''.join([self.base_url, '?', auth_chunk])
        response = self.client.get(url, content_type='application/json')
        self.assertEqual(response.status_code, 200)

        data = {'long_url': 'http://xxx.com'}
        response = self.client.post(url, json.dumps(data), 'application/json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response['Location'], "http://testserver/api/v1/url/1/")

        url = ''.join([self.base_url, '1/?', auth_chunk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)

        self.assertNotEqual(data['key'], '')
        self.assertNotEqual(data['key'], None)
