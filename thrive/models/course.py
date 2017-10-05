import datetime
import uuid
import nacl.pwhash

from mongoengine import *
from werkzeug.security import safe_str_cmp
from nacl.pwhash import verify_scryptsalsa208sha256

from thrive import app
from thrive.extensions.security.crypto.entropy import gen_salt
from thrive.extensions.security.crypto.message_integrity import compute_hash


# ------------------------------------------------------------------------------
# CLASS COURSE
# ------------------------------------------------------------------------------
class Course:
    
    """
        Represents a course that is been given in the determined educational 
        institution. 
    """

    course_id = StringField(max_length=40, required=True)

    title = StringField(max_length=256, required=True)

    coordinator_id = StringField(max_length=40, required=True)
    
    starts = DateTimeField(required=True)
    
    ends = DateTimeField(required=True)
    
    level = StringField(max_length=120, required=True)

    description = StringField(max_length=512, required=True)

