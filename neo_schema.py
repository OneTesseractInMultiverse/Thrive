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


"""
Types --------------------------------------------------------------------------

StringProperty
IntegerProperty
FloatProperty
BooleanProperty
ArrayProperty
DateProperty
DateTimeProperty
JSONProperty
AliasProperty

INDEXE -------------------------------------------------------------------------

unique_index
index
required
Default

"""


# Credentials
url = 'graph.subvertic.com:7687'
neo4j_username = 'neo4j'
neo4j_password = 'Awsx1Sedc2Drfv34'

config.DATABASE_URL = 'bolt://' + neo4j_username + ':' + neo4j_password + '@' + url


class User(StructuredNode):
    
    # --------------------------------------------------------------------------
    # CLASS PROPERTIES
    # --------------------------------------------------------------------------
    
    user_id = StringProperty(unique_index=True, required=True)
    name = StringProperty(required=True)
    last_name = StringProperty(required=True)
    email = StringProperty(unique_index=True, required=True)
    username = StringProperty(unique_index=True, required=True)
    password = StringProperty(required=True)
    
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
    
    
    
class Group(StructuredNode):
    
    group_id = StringProperty(unique_index=True, required=True)
    name = StringProperty(required=True)
    description = StringProperty(required=True)
    
    members = RelationshipTo('User', 'HAS')
                
    
    
"""
    user_id = StringProperty(unique_index=True, required=True)
    name = StringProperty(required=True)
    last_name = StringProperty(required=True)
    email = StringProperty(unique_index=True, required=True)
    username = StringProperty(unique_index=True, required=True)
    password = StringProperty(required=True)
"""
    
"""    
usr = User(
    user_id=str(uuid.uuid4()), 
    name="Pedro", 
    last_name="Guzman", 
    email="pedro@subvertic.com", 
    username="pedro.guzman"
)

usr.update_password("Wstinol123.")

usr.save()


grp = Group(
    group_id = str(uuid.uuid4()), 
    name = 'Administrators', 
    description = "Application Administrators - Full Access Group"
)
grp.save()

print('Created group...')

grp = Group.nodes.get(name='Administrators')
usr = User.nodes.get(user_id='b75084a3-f75d-4351-ae66-b727d7938f42')

print(grp.name)
print(usr.name)

grp.members.connect(usr)
grp.save()



"""

usr = User(
    user_id=str(uuid.uuid4()), 
    name="Pedro", 
    last_name="Guzman", 
    email="pedro@subvertic.com", 
    username="pedro.guzman"
)
usr.update_password("Wstinol123.")
usr.save()

grp = Group(
    group_id = str(uuid.uuid4()), 
    name = 'Administrators', 
    description = "Application Administrators - Full Access Group"
).save()


grp2 = Group(
    group_id = str(uuid.uuid4()), 
    name = 'Teachers', 
    description = "Application Administrators - Full Access Group"
).save()

usr.refresh()
grp.refresh()
grp2.refresh()

usr.groups.connect(grp)
usr.groups.connect(grp2)
usr.save()

grp.members.connect(usr)
grp.save()

grp2.members.connect(usr)
grp2.save()

