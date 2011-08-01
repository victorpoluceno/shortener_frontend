import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings_production'

import sys
sys.path.append('lib/shortener_worker')

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
