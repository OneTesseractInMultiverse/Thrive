from thrive import graph
from thrive.extensions.time import timestamp
from py2neo import Node, Relationship
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
    def __init__(self, node_type, **kwargs):
        self.node_type = node_type.upper()
        if 'id' in kwargs:
            self.__load()
        else:
            self.id = str(uuid.uuid4())
            for key, value in kwargs.items():
                setattr(self, key, value)
            self.is_persistent = False

    # -----------------------------------------------------------------------------------
    # PROPERTIES
    # -----------------------------------------------------------------------------------
    @property
    def properties(self):
        return self.__dict__.keys()

    # -----------------------------------------------------------------------------------
    # NODE
    # -----------------------------------------------------------------------------------
    @property
    def node(self):
        """
            This property fetches the current node state representation that exists within
            the persistent graph.
            :return: Node if found in graph
        """
        if self.is_persistent:
            return graph.find_one(self.node_type, 'id', self.id)
        else:
            return None

    # -----------------------------------------------------------------------------------
    # METHOD SAVE
    # -----------------------------------------------------------------------------------
    def save(self):
        """
            Persists current NodeEntity in the graph. This is done using merge function
            so that this method can be used for both, creation and updating data. 
            :return: True if operation succeeded
        """
        # First we create a node instance and
        node = Node(
            self.node_type,
            id=self.id
        )
        graph.merge(node)
        node['timestamp'] = timestamp()
        for attribute in self.properties:
            node[attribute] = self.__dict__[attribute]
        node.push()
        self.is_persistent = True
        return True

    # -----------------------------------------------------------------------------------
    # METHOD REL
    # -----------------------------------------------------------------------------------
    def link(self, edge_type, other_node):
        """
            Adds an edge to the graph parting from current node and arriving to the node
            provided as parameter. The relationship is of type edge_type.
            
            :param edge_type: The type of the relationship that will be created
            :param other_node: The destination node where the edge will arrive to. 
            :return: True is relationship was created successfully. False if relationship
                     was not created. 
        """
        if self.is_persistent:
            edge_type = edge_type.upper()
            relationship = Relationship(self.node, edge_type, other_node)
            graph.merge(relationship)
            return True
        return False

    # -----------------------------------------------------------------------------------
    # METHOD _LOAD
    # -----------------------------------------------------------------------------------
    def __load(self):
        """
            Fetched the data that is persisted in corresponding node in the Graph and 
            loads it into current instance of NodeEntity
            
            :return: True is data was successfully retrieved
        """
        data = self.node
        if data is not None:
            for key, value in data.items():
                setattr(self, key, value)
            self.is_persistent = True
            return True
        else:
            return False

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

    # -----------------------------------------------------------------------------------
    # CONSTRUCTOR METHOD
    # -----------------------------------------------------------------------------------
    def __init__(self, **kwargs):
        super(Student,  self).__init__(node_type='student', **kwargs)

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


