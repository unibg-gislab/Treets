#!/usr/bin/python
import sys
sys.path.insert(0, '/var/www/treets/treets')
from treets import app as application
application.config['APPLICATION_ROOT'] = '/treets'
