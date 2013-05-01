import logging
from lxml import etree
import webapp2

from util import memoized


prefixes = {'cli': "{jabber:client}",
            'prop': "{http://www.jivesoftware.com/xmlns/xmpp/properties}"}
query_str = ("/{cli}presence/{prop}properties/{prop}property[{prop}name='%s']"
             "/{prop}value/text()").format(**prefixes)


@memoized
def property_query(s):
    return etree.ETXPath(query_str % s)

def get_property(et, s):
    results = property_query(s)(et)
    if results:
        return results[0]
    else:
        return None

class AvailableHandler(webapp2.RequestHandler):
    def post(self):
        stanza = self.request.get('stanza')
        et = etree.fromstring(stanza)
        logging.info("Got event with mode: %r", get_property(et, 'mode'))
        logging.info("Full stanza: %r", stanza)

class UnavailableHandler(webapp2.RequestHandler):
    def post(self):
        logging.info("Got unavailable event: %r", self.request.get('stanza'))
