import urlparse
import urllib2
import re
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator, URL_VALIDATOR_USER_AGENT
from django.utils.encoding import smart_unicode


class ViewPathValidator(RegexValidator):
    regex = re.compile(
        r'^(((?!/)\S)+)$' , re.IGNORECASE) # option : accept everything except slash and spaces


class URLValidator(RegexValidator):
    regex = re.compile(
        r'(?!^//)' #dont accept start with double slash
        r'^('
          r'('
            r'(https?://|ftp://)' # start with 'http://'' or 'https://'' or 'ftp://'
            r'('
              r'(([A-Z0-9]\.?)+)|' # folowed by standard domain or just a name...
              r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or a ip number
            r')'
            r'(?::\d+)?' # with optional port
          r')|'
          r'(\.\.?)|'    # or start with '.(.)'
          r'(/{1})|'    # or start with unik '/' and non space char
          r'((?![/|\s]))'   # or at least by one non space char, nor '/'
        r')'  #end startwith
        r'((?!//)\S)*$' , re.IGNORECASE) # option : accept everything in fine except double slash

    def __init__(self, verify_exists=False, validator_user_agent=URL_VALIDATOR_USER_AGENT):
        super(URLValidator, self).__init__()
        self.verify_exists = verify_exists
        self.user_agent = validator_user_agent

    def __call__(self, value):
        try:
            super(URLValidator, self).__call__(value)
        except ValidationError, e:
            if value:
                value = smart_unicode(value)
                scheme, netloc, path, query, fragment = urlparse.urlsplit(value)
                url = urlparse.urlunsplit((scheme, netloc, path, query, fragment))
                super(URLValidator, self).__call__(url)
            else:
                raise
        else:
            url = value

        if self.verify_exists:
            headers = {
                "Accept": "text/xml,application/xml,application/xhtml+xml,text/html;q=0.9,text/plain;q=0.8,image/png,*/*;q=0.5",
                "Accept-Language": "en-us,en;q=0.5",
                "Accept-Charset": "ISO-8859-1,utf-8;q=0.7,*;q=0.7",
                "Connection": "close",
                "User-Agent": self.user_agent,
            }
            try:
                req = urllib2.Request(url, None, headers)
                u = urllib2.urlopen(req)
            except ValueError:
                raise ValidationError(_(u'Enter a valid URL.'), code='invalid')
            except: # urllib2.URLError, httplib.InvalidURL, etc.
                raise ValidationError(_(u'This URL appears to be a broken link.'), code='invalid_link')