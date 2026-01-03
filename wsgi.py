import sys
import os

sys.path.insert(0, '/home/anxoredesgria')

from www import create_app


_application = create_app()

def application(environ, start_response):
    environ['SCRIPT_NAME'] = '/appflask' 
    return _application(environ, start_response)