# A small file to make it easier to import stuff in "python manage.py shell"

# Settings
from erp.settings import *

# Inbuilt django imports
from django.http import *
from django.shortcuts import *
from django.template import *
from django.contrib import *
from django.contrib.auth import *
from django.template.loader import *

# Models
from dept.models import *
from users.models import *
from dash.models import *
from tasks.models import *

# Forms
from users.forms import *
from tasks.forms import *

# Views
from dept.views import *
from users.views import *
from dash.views import *
from tasks.views import *

# Utils
from misc.utilities import *
