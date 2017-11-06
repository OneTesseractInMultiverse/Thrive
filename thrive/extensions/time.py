from datetime import datetime
import os
import uuid


# ------------------------------------------------------------------------------
# FUNCTION TIMESTAMP
# ------------------------------------------------------------------------------
def timestamp():
    """
    """
    epoch = datetime.utcfromtimestamp(0)
    now = datetime.now()
    delta = now - epoch
    return delta.total_seconds()


# ------------------------------------------------------------------------------
# FUNCTION DATE
# ------------------------------------------------------------------------------
def date():
    """
    """
    return datetime.now().strftime('%Y-%m-%d')