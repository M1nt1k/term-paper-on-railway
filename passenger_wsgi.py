# -*- coding: utf-8 -*-
import os, sys
sys.path.insert(0, '/var/www/u1868048/data/www/mintik.site/railway')
sys.path.insert(1, '/var/www/u1868048/data/.venv/lib/python3.10/site-packages')
os.environ['DJANGO_SETTINGS_MODULE'] = 'railway.settings'
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
