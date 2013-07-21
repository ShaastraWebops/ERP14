#For simple dajax(ice) functionalities
from django.utils import simplejson
from misc.dajaxice.decorators import dajaxice_register
from misc.dajax.core import Dajax
from misc.dajaxice.utils import deserialize_form
# For rendering templates
from django.template import RequestContext
from django.template.loader import render_to_string

@dajaxice_register
def budgeting_modal(request):
    """
        Used to populate the Modal with Budgeting page
    """
    dajax = Dajax()
    
    html_content = render_to_string("finance/budgeting.html", locals(), RequestContext(request))
    dajax.remove_css_class('#id_modal', 'hide') # Show modal
    dajax.assign("#id_modal", "innerHTML", html_content) # Populate modal
    
    return dajax.json()
 
