from neomodel import (
    config, 
    StructuredNode, 
    StringProperty,
    BooleanProperty,
    IntegerProperty,
    FloatProperty,
    DateProperty,
    UniqueIdProperty, 
    RelationshipTo, 
    RelationshipFrom,
    One,
    OneOrMore,
    ZeroOrOne
)

from nacl.pwhash import verify_scryptsalsa208sha256, scryptsalsa208sha256_str
from datetime import date, datetime
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
    is_active = BooleanProperty(required=True)
    
    is_anonymous = False
    is_authenticated = True
    
    # RELATIONS
    groups = RelationshipTo('Group', 'IS_MEMBER_OF')
    courses = RelationshipTo('Course', 'TEACHES')

    # --------------------------------------------------------------------------
    # DGET ID
    # --------------------------------------------------------------------------
    def get_id(self):
        return self.user_id
   
    # --------------------------------------------------------------------------
    # DICTIONARY PROPERTY
    # --------------------------------------------------------------------------
    @property
    def dictionary(self):
        output = {}
        for prop in self.__dict__.keys():
            if prop is not 'password' and not prop.startswith('__'):
                output[prop] = getattr(prop)
        return output
                
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
        try:
            proposed = password.encode('utf-8')
            hashed = self.password.encode('utf-8')
            return verify_scryptsalsa208sha256(hashed, proposed)
        except Exception as ex:
            return False
        
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

    # --------------------------------------------------------------------------
    # DICTIONARY PROPERTY
    # --------------------------------------------------------------------------
    @property
    def dictionary(self):
        output = {}
        for prop in self.__dict__.keys():
            if not prop.startswith('__'):
                output[prop] = getattr(self, prop)
        return output
        
    
# ##############################################################################
# BUSINESS OBJECTS
# ##############################################################################
# (year, month, day)

class LegalGuardian(StructuredNode):

    # Attributes
    personal_id = StringProperty(unique_index=True, required=True)
    name = StringProperty(required=True)
    last_name = StringProperty(required=True)
    second_last_name = StringProperty(required=True)
    phone_number = StringProperty(required=True, index=True)
    email = StringProperty()
    address = StringProperty()

    # Edges
    dependents = RelationshipTo('Student', 'IS_RESPONSIBLE_FOR')


# ------------------------------------------------------------------------------
# CLASS STUDENT
# ------------------------------------------------------------------------------
class Student(StructuredNode):

    # Attributes
    student_id = StringProperty(unique_index=True, required=True)
    personal_id = StringProperty(unique_index=True, required=True)
    date_of_birth = DateProperty(required=True)
    name = StringProperty(required=True, index=True)
    last_name = StringProperty(required=True, index=True)
    second_last_name = StringProperty(required=True)
    education_level = StringProperty(required=True, index=True)
    education_level_year = StringProperty(required=True, index=True)
    active = BooleanProperty(required=True)

    # Edges
    legal_guardians = RelationshipTo('LegalGuardian', 'IS_DEPENDENT_OF')
    courses = RelationshipTo('Course', 'IS_TAKING')
    past_courses = RelationshipTo('Course', 'TOOK')

    # --------------------------------------------------------------------------
    # DICTIONARY PROPERTY
    # --------------------------------------------------------------------------
    @property
    def dictionary(self):
        """
            Gets a dictionary representation of the current instance of Student
            :return: 
        """
        output = {}
        for prop in self.__dict__.keys():
            if not prop.startswith('__'):
                output[prop] = getattr(prop)
        return output

    # --------------------------------------------------------------------------
    # SET DATE OF BIRTH
    # --------------------------------------------------------------------------
    def set_date_of_birth(self, day, month, year):
        """
            Sets the date object in Student class
            
            :param day: The day
            :param month: The month
            :param year: The year
            :return: True if well formatted and valid date provided. False if not.
            
        """
        try:
            self.date_of_birth = date(year, month, day)
            return True
        except Exception as ex:
            # TODO good exception handling!!!
            print(ex)
            return False
            

# ------------------------------------------------------------------------------
# CLASS COURSE
# ------------------------------------------------------------------------------
class Course(StructuredNode):
    
    # ATTRIBUTES ---------------------------------------------------------------
    course_id = StringProperty(unique_index=True, required=True)
    title = StringProperty(required=True, index=True)
    description = StringProperty(required=True)
    year = IntegerProperty(required=True, index=True)
    education_level_year = StringProperty(required=True, index=True)
    
    # RELATIONS ----------------------------------------------------------------
    taught_by = RelationshipTo('User', 'IS_TAUGHT_BY')
    students = RelationshipTo('Student', 'IS_BEING_TAKEN_BY')
    period = RelationshipTo('Period', 'IS_GIVEN_DURING', cardinality=One)
 
 
# ------------------------------------------------------------------------------
# CLASS COURSE
# ------------------------------------------------------------------------------    
class Grade(StructuredNode):
    
    # ATTRIBUTES ---------------------------------------------------------------
    passing = BooleanProperty(required=True)
    total_points = FloatProperty(required=True)
    value_percentage = FloatProperty(required=True)
    date = DateProperty(required=True)
    
    # RELATIONS ----------------------------------------------------------------
    student = RelationshipTo('Student', 'WAS_OBTAINED_BY', cardinality=One)
    course = RelationshipTo('Course', 'WAS_OBTAINED_IN', cardinality=One)
    period = RelationshipTo('Period', 'WAS_OBTAINED_DURING', cardinality=One)
    
    
# ------------------------------------------------------------------------------
# CLASS COURSE
# ------------------------------------------------------------------------------    
class Period(StructuredNode):
    
    # ATRIBUTES ----------------------------------------------------------------
    
    year = IntegerProperty(index=True, required=True)
    denominator = IntegerProperty(index=True, required=True)
    number = IntegerProperty(index=True, required=True)

    # RELATIONS ----------------------------------------------------------------
    grades = RelationshipTo('Grade', 'HAS')
    courses = RelationshipTo('Course', 'HAS')
    
    # --------------------------------------------------------------------------
    # METHOD STATE IS VALID
    # --------------------------------------------------------------------------
    def state_is_valid(self):
        if self.year < 2016:
            return False
        if self.number > self.denominator:
            return False
        return True

# ##############################################################################
# TRANSACTIONAL OBJECTS
# ##############################################################################

# ##############################################################################
# STATE OBJECTS
# ##############################################################################
