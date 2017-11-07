import datetime
import uuid
import nacl.pwhash

from datetime import date
from nacl.pwhash import verify_scryptsalsa208sha256
from py2neo.ogm import GraphObject, Property, RelatedTo, RelatedFrom
from thrive import graph, login_manager

# ==============================================================================
# CLASS USER
# ==============================================================================

class User(GraphObject):
    
    # Indexes ------------------------------------------------------------------
    
    __primarykey__ = "user_id"
    __primarylabel__ = "USER"
    
    # Properties ---------------------------------------------------------------
    
    user_id = Property()
    name = Property()
    last_name = Property()
    email = Property()
    username = Property()
    password = Property()
    
    is_authenticated = True
    is_active = True
    is_anonymous = False
    
    # Relations ----------------------------------------------------------------
    groups = RelatedTo("GROUP", "MEMBER_OF")
    courses = RelatedTo("COURSE", "TEACHES")
    
    # --------------------------------------------------------------------------
    # METHOD INIT
    # --------------------------------------------------------------------------
    def __init__(self, **kwargs):
        """
        """
        for key, value in kwargs.items():
                setattr(self, key, value)
    
    # --------------------------------------------------------------------------
    # METHOD LT
    # --------------------------------------------------------------------------
    def __lt__(self, other):
        """
        """
        return self.user_id < other.user_id
        
    # --------------------------------------------------------------------------
    # METHOD SAVE TO
    # --------------------------------------------------------------------------
    def save_to(self, dest_graph):
        dest_graph.merge(self)
        
    # --------------------------------------------------------------------------
    # METHOD UPDATE
    # --------------------------------------------------------------------------
    def update(self, dest_graph):
        dest_graph.push(self)
    
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
        self.password = nacl.pwhash.scryptsalsa208sha256_str(password.encode('utf-8')).decode('utf-8')
        return True
        
    # --------------------------------------------------------------------------
    # METHOD UPDATE EMAIL
    # --------------------------------------------------------------------------
    def update_email(self, email):
        """
            Updates the user's email with a new email.
            :param email: The new email address that is going to be assigned to the
                          user.
            :return: True if the email was updated successfully
        """
        self.email = email
        return True
        
# ==============================================================================
# CLASS GROUP
# ==============================================================================
class Group(GraphObject):
    
    # Indexes ------------------------------------------------------------------
    
    __primarykey__ = "group_id"
    __primarylabel__ = "GROUP"
    
    
    # Properties ---------------------------------------------------------------
    group_id = Property()
    name = Property()
    description = Property()
    
    # Relations ----------------------------------------------------------------
    members = RelatedTo("USER", "HAS_USER")
    
    # --------------------------------------------------------------------------
    # METHOD LT
    # --------------------------------------------------------------------------
    def __lt__(self, other):
        """
        """
        return self.user_id < other.user_id
    
    
    # --------------------------------------------------------------------------
    # METHOD INIT
    # --------------------------------------------------------------------------
    def __init__(self, **kwargs):
        """
        """
        for key, value in kwargs.items():
                setattr(self, key, value)
                
    # --------------------------------------------------------------------------
    # METHOD ADD MEMBER
    # --------------------------------------------------------------------------        
    def add_member(self, new_member):
        self.members.add(new_member)
        
        
# ==============================================================================
# FUNCTIONS
# ==============================================================================
# ------------------------------------------------------------------------------
# GET USER BY ID
# ------------------------------------------------------------------------------
@login_manager.user_loader
def get_user_by_id(user_id):
    """
        Tries to find a given instance of user by using its username. If the user
        exists and was found, an instance of user is returned, else, None is
        returned meaning that the system was unable to find a user with the given
        username.
    """
    return User.select(graph, user_id).first()

# ------------------------------------------------------------------------------
# GET USER BY USERNAME
# ------------------------------------------------------------------------------
def get_user_by_username(usrname):
    """
        Tries to find a given instance of user by using its username. If the user
        exists and was found, an instance of user is returned, else, None is
        returned meaning that the system was unable to find a user with the given
        username.
    """
    try:
        return User.select(graph).where("_.username =~ '" + usrname + "'").first()
    except Exception as ex:
        return None
        
# ------------------------------------------------------------------------------
# BUILD_ACCOUNT
# ------------------------------------------------------------------------------
def build_account(account_data):
    """
        Validates a given dictionary containing information required to create 
        a new user account and if it is correct, returns a instance of User, if 
        not or any of the required parameters are missing, then None is returned
        
        :param account_data: A dictionary containing the necessary information 
                to create a new user account. 
        :return: None if some required data is missing and instance of User if
                all data is correct
    """

    try:
        name = account_data['name']
        if name is None:
            return None

        last_name = account_data['last_name']
        if last_name is None:
            return None

        username = account_data['username']
        if username is None:
            return None

        email = account_data['email']
        if email is None:
            return None

        password = account_data['password']
        if password is None:
            return None

        user = User(
            user_id=str(uuid.uuid4()),
            name=name,
            last_name=last_name,
            username=username,
            email=email
        )

        # We set the password by calling the update function that handles
        # proper hashing of the password so we never store the actual
        # password

        user.update_password(password)
        return user

    except:
        return None