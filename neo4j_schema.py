from py2neo import Graph, authenticate
from py2neo.ogm import GraphObject, Property, RelatedTo, RelatedFrom
from nacl.pwhash import verify_scryptsalsa208sha256, scryptsalsa208sha256_str
from datetime import date
import uuid

# Credentials
url = 'graph.subvertic.com:7474'
neo4j_username = 'neo4j'
neo4j_password = 'Awsx1Sedc2Drfv34'

# Fetch connection
authenticate(
    url,
    neo4j_username,
    neo4j_password
)

# Connect to graph
graph = Graph(
    'http://' + url,
    bolt=False
)

# ==============================================================================
# CLASS USER
# ==============================================================================

class User(GraphObject):
    
    # Indexes ------------------------------------------------------------------
    
    __primarykey__ = "user_id"
    __primarylabel__ = "User"
    
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
    groups = RelatedTo("Group", "MEMBER_OF")
    #courses = RelatedTo("COURSE", "TEACHES")
    
    # --------------------------------------------------------------------------
    # METHOD INIT
    # --------------------------------------------------------------------------
    def __init__(self, **kwargs):
        """
        """
        for key, value in kwargs.items():
                setattr(self, key, value)
                
    def add_to_group(self, group):
        self.groups.add(self)
    
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
        self.password = scryptsalsa208sha256_str(password.encode('utf-8')).decode('utf-8')
        return True
        
# ==============================================================================
# CLASS GROUP
# ==============================================================================
class Group(GraphObject):
    
    # Indexes ------------------------------------------------------------------
    
    __primarykey__ = "group_id"
    __primarylabel__ = "Group"
    
    
    # Properties ---------------------------------------------------------------
    group_id = Property()
    name = Property()
    description = Property()
    
    # Relations ----------------------------------------------------------------
    members = RelatedTo("User", "HAS_USER")
    
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
        
# ==============================================================================
# FUNCTIONS
# ==============================================================================
# ------------------------------------------------------------------------------
# GET USER BY ID
# ------------------------------------------------------------------------------
def get_user_by_id(user_id):
    """
        Tries to find a given instance of user by using its username. If the user
        exists and was found, an instance of user is returned, else, None is
        returned meaning that the system was unable to find a user with the given
        username.
    """
    return User.select(graph, user_id)
    
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
  
        
def get_group_by_name(usrname):
    """
        Tries to find a given instance of user by using its username. If the user
        exists and was found, an instance of user is returned, else, None is
        returned meaning that the system was unable to find a user with the given
        username.
    """
    try:
        return User.select(graph).where("_.username =~ '" + usrname + "'").first()
    except Exception as ex:
        print(ex)
        return None

    
"""    
uid = str(uuid.uuid4())   

print('Creating group...')
group = Group(
        group_id = str(uuid.uuid4()),
        name = 'Admin',
        description = 'Administradores de Trive'
    )
    
group.save_to(graph)
        
print('Creating user...')      
user = User(
        user_id = uid,
        name = "John",
        last_name = "Doe", 
        username = "john.doe@thrive-edu.org", 
    )

print('User createed...')
user.update_password('Wstinol123.')

print('Saving to graph...')
user.save_to(graph)

#print('Adding user to group...')
#group.add_member(user)

#print('Saving changes...')
#group.update_to(graph)

print('Saved!')
"""
usr = list(User.select(graph).where("_.name =~ 'J.*'"))[0]
grp = list(Group.select(graph).where("_.name =~ 'Teachers'"))[0]

print(grp.name)

#grp.members.add(usr)
#graph.push(grp)

usr.groups.add(grp)
graph.push(usr)

"""
group = Group(
        group_id = str(uuid.uuid4()),
        name = 'Directors',
        description = 'Directors Group'
    )
    
group.members.add(usr)
graph.merge(group)

usr.groups.add(group)
graph.merge(usr)
"""
