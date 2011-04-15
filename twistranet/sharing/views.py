"""
Tags-specific views, including JSON stuff.
"""
import urllib
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.template import RequestContext, loader
from django.shortcuts import *
from django.contrib import messages
from django.utils.translation import ugettext as _
from django.conf import settings
from django.core.paginator import Paginator, InvalidPage
from django.db.models import Q

try:
    # python 2.6
    import json
except:
    # python 2.4 with simplejson
    import simplejson as json

from twistranet.twistapp.models import Content, Account
from twistranet.twistapp.forms import form_registry
from twistranet.twistapp.lib.log import *
from twistranet.core.views import *



class LikeToggleView(BaseObjectActionView):
    """
    Individual Content View.
    """
    model_lookup = Content
    name = "like_toggle_by_id"


    def render_view(self,):
        """
        """
        likes = self.content.likes()
        n_likes = likes['n_likes']
        if not likes['i_like']:
            self.content.like()
            ilike = True
            n_likes += 1
        else:
            self.content.unlike()
            ilike = False
            n_likes -= 1
        data =  {'i_like' : ilike, 'n_likes' : n_likes}
        return HttpResponse( json.dumps(data),
                             mimetype='text/plain')

