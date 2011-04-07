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
from models import Tag


class LikeToggleView(BaseObjectActionView):
    """
    Individual Content View.
    """
    model_lookup = Content
    name = "like_toggle_by_id"

    def prepare_view(self, *args, **kw):
        """
        Prepare tag view.
        Basically, tag view is just a search of the most relevant content matching this tag.
        We also provide a paginator to browse results easily.
        """
        super(LikeToggleView, self).prepare_view(*args, **kw)
        if not self.content.likes['i_like']:
            self.content.like()
        else:
            self.content.unlike()

