from thrive import graph
from thrive.extensions.time import timestamp
import uuid
import datetime
import abc


# ---------------------------------------------------------------------------------------
# CLASS GRAPH ENTITY
# ---------------------------------------------------------------------------------------
class GraphEntity:

    """
        Defines a graph entity that can be persisted as a node within Neo4j
    """

    # -----------------------------------------------------------------------------------
    # CLASS CONSTRUCTOR
    # -----------------------------------------------------------------------------------
    def __init__(self, **kwargs):
        """
            :param kwargs: 
        """
        if 'id' in kwargs:
            self.__load()
        else:
            self.id = uuid.uuid4()
            for key, value in kwargs.items():
                setattr(self, key, value)

    # -----------------------------------------------------------------------------------
    # METHOD SAVE
    # -----------------------------------------------------------------------------------
    @abc.abstractmethod
    def save(self):

        pass

    # -----------------------------------------------------------------------------------
    # METHOD _LOAD
    # -----------------------------------------------------------------------------------
    @abc.abstractmethod
    def __load(self):
        pass

    # -----------------------------------------------------------------------------------
    # METHOD MODEL STATE VALID
    # -----------------------------------------------------------------------------------
    @abc.abstractmethod
    def model_state_valid(self):
        pass


# =======================================================================================
# CLASS STUDENT
# =======================================================================================
class Student(GraphEntity):

    def __init__(self, **kwargs):
        super(Student, self).__init__(**kwargs)

    # -----------------------------------------------------------------------------------
    # METHOD MODEL STATE VALID
    # -----------------------------------------------------------------------------------
    def model_state_valid(self):
        """
            This method validates that all required or mandatory properties are present in 
            current instance of the class.
            :return: True is all required properties exist in current instance, False if one
            or more is not present
        """

        # First we get a list of all current properties in the instance
        properties = self.__dict__.keys()

        # Now we validate that the properties are present
        if 'id' in properties and \
                'personal_id' in properties and \
                'name' in properties and \
                'last_name' in properties and \
                'second_last_name' in properties and \
                'birth_day' in properties and \
                'birth_month' in properties and \
                'birth_year' in properties:
            return True
        else:
            return False

    # -----------------------------------------------------------------------------------
    # METHOD DATE OF BIRTH
    # -----------------------------------------------------------------------------------
    def date_of_birth(self):
        """
            Returns the datetime representing the date of birth of the student
            :return: 
        """
        if self.birth_day is not None and self.birth_month is not None and self.birth_year is not None:
            return datetime.date(
                year=self.birth_year,
                month=self.birth_month,
                day=self.birth_day
            )
        return None

    # -----------------------------------------------------------------------------------
    # METHOD _LOAD
    # -----------------------------------------------------------------------------------
    def __load(self):
        """
            
            :return: 
        """
        if self.id is not None:
            self.is_persistent = True
            return True
        else:
            self.is_persistent = False
            return False
