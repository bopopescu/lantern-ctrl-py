import json
import logging
import cgi

import webapp2
from google.appengine.api import xmpp

import boto
from boto.sqs.message import RawMessage

import mandrill

import presence
import secrets


class Cron(webapp2.RequestHandler):
    logging.getLogger('boto').setLevel(logging.INFO)
    def get(self):
        sqs = boto.connect_sqs(secrets.awsAccessKeyId,
                               secrets.awsSecretKey)
        q = sqs.get_queue('colaprova')
        #XXX: Use JsonMessage.
        q.set_message_class(RawMessage)
        msgs = sqs.receive_message(q)
        if msgs:
            for msg in msgs:
                logging.info("Message: " + msg.get_body())
                # Now I would need to deal with this and delete it.
        else:
            logging.info("No messages for ya.")

class Mandrill(webapp2.RequestHandler):
    def get(self):
        invitee_email = self.request.get("invitee") or "euccastro@gmail.com"
        inviter_email = "aranhoide@gmail.com"
        m = mandrill.Mandrill(
                apikey=secrets.mandrillApiKey,
                debug=True)
        msg = {'subject': "Ei como vai?",
               'from_email': 'invite@getlantern.org',
               'from_name': "Lantern Beta",
               'to': [{'email': invitee_email}],
               'track_opens': False,
               'track_clicks': False,
               'auto_text': True,
               'url_slip_qs': True,
               'preserve_recipients': False,
               'bcc_address': 'aranhoide@gmail.com',
               'global_merge_vars': mergevarize(
                   {'INVITER_EMAIL': inviter_email,
                    'INVITER_NAME': "Estevo",
                    'OSXINSTALLERURL': 'https://example.com/lantern.dmg',
                    'WININSTALLERURL': 'https://example.com/lantern.exe',
                    'DEB32INSTALLERURL':
                        'https://example.com/lantern32.deb',
                    'DEB64INSTALLERURL':
                        'https://example.com/lantern64.deb'})}

        res = self.response.write(
                m.messages.send_template('cloud-invite', [], msg))
        self.response.write(cgi.escape(repr(res)))

def mergevarize(d):
    return [{'name': k, 'content': v}
            for k, v in d.iteritems()]

app = webapp2.WSGIApplication([('/_ah/xmpp/presence/available/',
                                presence.AvailableHandler),
                               ('/_ah/xmpp/presence/unavailable/',
                                presence.UnavailableHandler),
                               ('/cron', Cron),
                               ('/mandrill', Mandrill)],
                              debug=True)
