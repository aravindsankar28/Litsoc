import os, sys
apache_configuration = os.path.dirname(__file__)
project = os.path.dirname(apache_configuration)
workspace = os.path.dirname(project)
sys.path.append(workspace)
#Append django itself
sys.path.append('/usr/local/lib/python2.6/dist-packages/Django-1.3.1-py2.6.egg/django')
os.environ['DJANGO_SETTINGS_MODULE'] = 'lit.apache.settings_production'
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
ROOT_URLCONF = 'lit.apache.urls_production'
