# For simple dajax(ice) functionalities
from django.utils import simplejson
from misc.dajaxice.decorators import dajaxice_register
from misc.dajax.core import Dajax
# For rendering templates
from django.template import Template, Context, RequestContext
from django.shortcuts import render
from django.template.loader import get_template
# From models
from users.models import ERPUser
# From Misc to show bootstrap alert
from misc.utilities import show_alert

