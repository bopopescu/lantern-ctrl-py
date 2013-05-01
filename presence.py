import json
import logging
from lxml import etree

import webapp2
from google.appengine.api import xmpp

import const
import data
import util


prefixes = {'cli': "{jabber:client}",
            'prop': "{http://www.jivesoftware.com/xmlns/xmpp/properties}"}
query_str = ("/{cli}presence/{prop}properties/{prop}property[{prop}name='%s']"
             "/{prop}value/text()").format(**prefixes)


@util.memoized
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
        sender_jid = self.request.get('from')
        logging.info("Got request from jid %r to %r", sender_jid, self.request.get('to'))
        sender_email = util.userid_from_jid(sender_jid)
        if not data.is_invited(sender_email):
            logging.info("Not invited!")
            send_response(sender_jid, {const.INVITED: False})
            return
        stanza = self.request.get('stanza')
        et = etree.fromstring(stanza)
        logging.info("Got event with mode: %r", get_property(et, 'mode'))
        logging.info("Full stanza: %r", stanza)

class UnavailableHandler(webapp2.RequestHandler):
    def post(self):
        logging.info("Got unavailable event: %r", self.request.get('stanza'))

def send_response(jid, body):
    xmpp.send_message([jid],
                      json.dumps(body),
                      const.CTRL_JID,
                      xmpp.MESSAGE_TYPE_HEADLINE)
