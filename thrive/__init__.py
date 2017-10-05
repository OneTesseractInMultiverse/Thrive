#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import yaml
from flask import Flask as FlaskBase, Config as ConfigBase
from flask_mongoengine import MongoEngine
from flask_jwt_extended import JWTManager
from flask_login import LoginManager
from py2neo import Graph


# ------------------------------------------------------------------------------
# CLASS CONFIG
# ------------------------------------------------------------------------------
class Config(ConfigBase):
    
    """
        Extends Flask's config class to include a 'from_yaml' method that allows
        the application to load configurations from a YAML file. 
    """
    
    # --------------------------------------------------------------------------
    # METHOD FROM_YAML
    # --------------------------------------------------------------------------
    def from_yaml(self, config_file, mode):
        
        """
            Reads a yaml configuration file and loads the configuration values 
            found into Flask's configuration. 
        """
        
        env = os.environ.get('FLASK_ENV', mode)
        self['ENVIRONMENT'] = env.lower()
        with open(config_file) as file:
            configuration = yaml.load(file)
        configuration.get(env, configuration)
        for key in configuration:
            if key.isupper():
                self[key] = configuration[key]
       

# ------------------------------------------------------------------------------
# CLASS GARNET
# ------------------------------------------------------------------------------
class Garnet(FlaskBase):
    """
        Extends Flask to support YAML configuration file. And some other Garnet
        specific features.
    """
    
    def make_config(self, instance_relative=False):
        """
            Makes the configuration location
        """
        root_path = self.root_path
        if instance_relative:
            root_path = self.instance_path
        return Config(root_path, self.default_config)


# ------------------------------------------------------------------------------
# SETUP GENERAL APPLICATION
# ------------------------------------------------------------------------------
__version__ = '1.0.0'
app = Garnet('Thrive')
app.config.from_object('config')

login_manager = LoginManager()
login_manager.init_app(app)
 
# ------------------------------------------------------------------------------
# SETUP MONGO DATABASE
# ------------------------------------------------------------------------------   
db = MongoEngine(app)

# ------------------------------------------------------------------------------
# SETUP MNEO4J DATABASE
# ------------------------------------------------------------------------------

url = os.environ.get('GRAPHENEDB_URL', 'http://localhost:7474')
neo4j_username = os.environ.get('NEO4J_USERNAME')
neo4j_password = os.environ.get('NEO4J_PASSWORD')

graph = Graph(url + '/db/data/', username=neo4j_username, password=neo4j_password)
# ------------------------------------------------------------------------------
# SETUP JWT
# ------------------------------------------------------------------------------

jwt = JWTManager(app) 

# ------------------------------------------------------------------------------
# LOAD ENDPOINTS
# ------------------------------------------------------------------------------
from thrive.endpoints import *
from thrive.controllers import *
