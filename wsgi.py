#!/usr/bin/env python
"""
WSGI config for openshift project.
It exposes the WSGI callable as a module-level variable named ``application``.
For more information on this file, see
https://docs.djangoproject.com/en/1.6/howto/deployment/wsgi/
"""
import os
import sys

os.environ['DJANGO_SETTINGS_MODULE'] = 'geartest4.settings'
ON_PAAS = 'OPENSHIFT_REPO_DIR' in os.environ

if 'OPENSHIFT_REPO_DIR' in os.environ:
    sys.path.append(os.path.join(os.environ['OPENSHIFT_REPO_DIR'], 'geartest4'))
    virtenv = os.environ['OPENSHIFT_PYTHON_DIR'] + '/virtenv/venv/'
    os.environ['PYTHON_EGG_CACHE'] = os.path.join(virtenv, 'lib/python3.3/site-packages')
    

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()