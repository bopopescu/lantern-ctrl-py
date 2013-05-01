from google.appengine.ext import ndb


class LanternUser(ndb.Model):
    id = ndb.StringProperty()
    directBytes = ndb.IntegerProperty(default=0)
    bytesProxied = ndb.IntegerProperty(default=0)
    directRequests = ndb.IntegerProperty(default=0)
    requestsProxied = ndb.IntegerProperty(default=0)
    created = ndb.DateTimeProperty(auto_now_add=True)
    countryCodes = ndb.StringProperty(repeated=True)
    invites = ndb.IntegerProperty(default=0)
    degree = ndb.IntegerProperty()
    sponsor = ndb.StringProperty()
    everSignedIn = ndb.BooleanProperty(default=False)
    lastAccessed = ndb.DateTimeProperty(auto_now=True)
    instancesSignedIn = ndb.IntegerProperty(default=0)
    instanceIds = ndb.StringProperty(repeated=True)
    installerLocation = ndb.StringProperty()

@ndb.transactional
def create_initial_user():
    root_email = 'aranhoide@gmail.com'
    if ndb.Key('LanternUser', root_email).get() is not None:
        logging.warning("Root user %s already exists.", root_email)
        return
    LanternUser(id=root_email,
                degree=1,
                sponsor=root_email).put()

def is_invited(email):
     return ndb.Key('LanternUser', email).get() is not None
