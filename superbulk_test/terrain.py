import os

from django.core.management import call_command
from lettuce import *


@before.harvest
def create_db(variables):
    call_command('syncdb', interactive=False, verbosity=0)


@after.harvest
def drop_db(vars):
    os.remove('db.sqlite3')