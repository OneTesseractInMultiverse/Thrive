from neomodel import (
    config, 
    StructuredNode, 
    StringProperty, 
    IntegerProperty,
    UniqueIdProperty, 
    RelationshipTo, 
    RelationshipFrom
)

from nacl.pwhash import verify_scryptsalsa208sha256, scryptsalsa208sha256_str
from datetime import date
import uuid


# ##############################################################################
# IDENTITY OBJECTS
# ##############################################################################

# ------------------------------------------------------------------------------
# CLASS USER
# ------------------------------------------------------------------------------
class User(StructuredNode):
    
    # --------------------------------------------------------------------------
    # CLASS PROPERTIES
    # --------------------------------------------------------------------------
    
    # PROPERTIES
    user_id = StringProperty(unique_index=True, required=True)
    name = StringProperty(required=True)
    last_name = StringProperty(required=True)
    email = StringProperty(unique_index=True, required=True)
    username = StringProperty(unique_index=True, required=True)
    password = StringProperty(required=True)
    
    # RELATIONS
    groups = RelationshipTo('Group', 'IS_MEMBER_OF')
                
    # --------------------------------------------------------------------------
    # METHOD AUTHENTICATE
    # --------------------------------------------------------------------------
    def authenticate(self, password):
        """
            Compares the given password in a secure way with a value stored in
            database to determine if the password is correct or not.
            
            :param password: The password to be verified if it is the correct password
                   for the given user.
                   
            :return: True if the authentication was successful and the password is
                     correct
        """
        proposed = password.encode('utf-8')
        hashed = self.password.encode('utf-8')
        return verify_scryptsalsa208sha256(hashed, proposed)
        
    # --------------------------------------------------------------------------
    # METHOD UPDATE PASSWORD
    # --------------------------------------------------------------------------
    def update_password(self, password):
        """
            Hashes and securely stores the password in a way that can be verifiable
            but cannot be decrypted.
            
            :param password: The password that will be set to be used as auth mechanism
                             for the user.
                             
            :return:         True if operation completed successfully
        """
        self.password = scryptsalsa208sha256_str(password.encode('utf-8')).decode('utf-8')
        return True
  
# ------------------------------------------------------------------------------
# CLASS GROUP
# ------------------------------------------------------------------------------       
class Group(StructuredNode):
    
    # PROPERTIES
    group_id = StringProperty(unique_index=True, required=True)
    name = StringProperty(required=True, unique_index=True)
    description = StringProperty(required=True)
    
    # RELATIONS
    members = RelationshipTo('User', 'HAS')
    
        
    
# ##############################################################################
# BUSINESS OBJECTS
# ##############################################################################

# ##############################################################################
# TRANSACTIONAL OBJECTS
# ##############################################################################

# ##############################################################################
# STATE OBJECTS
# ##############################################################################