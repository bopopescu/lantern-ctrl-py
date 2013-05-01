from google.appengine.api import app_identity


CTRLID = app_identity.get_application_id()
CTRL_JID = '%s@appspot.com' % CTRLID

# Shared with the client through lantern-common.
INVITED = 'invd'
