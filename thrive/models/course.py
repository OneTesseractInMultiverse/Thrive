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

    course_id = StringField(max_length=40, required=True)

    title = StringField(max_length=120, required=True)

    professor_id = StringField(max_length=40, required=True)

