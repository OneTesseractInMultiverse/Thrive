import datetime
import uuid
import nacl.pwhash

from mongoengine import *
from werkzeug.security import safe_str_cmp
from nacl.pwhash import verify_scryptsalsa208sha256

from thrive import app
from thrive.extensions.security.crypto.entropy import gen_salt
from thrive.extensions.security.crypto.message_integrity import compute_hash