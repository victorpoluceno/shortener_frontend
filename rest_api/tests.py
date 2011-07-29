import json
import urllib

from django.test import TestCase
from django.test.client import Client

from django.contrib.auth.models import User

from tastypie.models import ApiKey

from rest_api.models import Url
from rest_api.tasks import url_short, url_update, url_request, \
        UrlAlreadyUpdatedError
from rest_api.backend import Request

from celery.task.sets import subtask
from celery.task import task


class TasksTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('tests', \
                email='victorpoluceno@gmail.com')
        self.user.is_superuser = True
        self.user.is_staff = True
        self.user.save()

        self.url = Url.objects.create(long_url='hakta.com')
        self.url.save()

    def test_url_short_task(self):
        result = url_short.delay(self.url.id)
        url_updated = Url.objects.get(pk=self.url.id)
        self.assertNotEqual(url_updated.key, '')
        self.assertNotEqual(url_updated.key, None)
   
    def test_url_update_task(self):
        url = Url.objects.create(long_url='test.com')
        url.save()
        url_update.delay(url.id, 't99')
        url_updated = Url.objects.get(pk=url.id)
        self.assertEqual(url_updated.key, 't99')

        result = url_update.delay(9999, '')
        self.assertEqual(result.failed(), True)
        self.assertEqual(isinstance(result.result, Url.DoesNotExist), True)

        url = Url.objects.create(long_url='test2.com')
        url.key = 'xxx'
        url.save()
        result = url_update.delay(url.id, 'zzz')
        self.assertEqual(result.failed(), True)
        self.assertEqual(isinstance(result.result, UrlAlreadyUpdatedError), True)

    def test_url_request_task(self):
        @task
        def test_callback(url_id, short_url):
            self.assertEqual(url_id, self.url.id)
            self.assertNotEqual(short_url, '')
            self.assertNotEqual(short_url, None)

        url_request.delay(self.url.id, callback=subtask(test_callback))

        result = url_request.delay(9999, test_callback)
        self.assertEqual(result.failed(), True)
        self.assertEqual(isinstance(result.result, Url.DoesNotExist), True)
