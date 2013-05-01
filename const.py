from google.appengine.api import app_identity


CTRLID = app_identity.get_application_id()
CTRL_JID = '%s@appspot.com' % CTRLID

# Shared with the client through lantern-common.
UPDATE_KEY = 'uk'
UPDATE_VERSION_KEY = 'number'
UPDATE_URL_KEY = 'url'
UPDATE_MESSAGE_KEY = 'message'
UPDATE_RELEASED_KEY = 'released'
INVITES_KEY = 'invites'
INVITED_EMAIL = 'invem'
INVITEE_NAME = 'inv_name'
INVITER_NAME = 'invr_name'
INVITER_REFRESH_TOKEN = 'invr_refrtok'
INVITED = 'invd'
INVITED_KEY = 'invited'
FAILED_INVITES_KEY = 'failed_invites'
INVITE_FAILED_REASON = 'reason'
