import uuid
from functools import wraps
from flask import jsonify, render_template
from flask_login import current_user
from thrive import login_manager, app
from thrive.models.graph import User, Group

"""
    This module contains helper functions that perform operations related to 
    manipulation and retrieval of Identity and Access Management objects. 
"""


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
    return User.nodes.get_or_none(user_id=user_id)
        

# ------------------------------------------------------------------------------
# GET USER BY USERNAME
# ------------------------------------------------------------------------------
def get_user_by_username(user_name):
    """
        Tries to find a given instance of user by using its username. If the user
        exists and was found, an instance of user is returned, else, None is
        returned meaning that the system was unable to find a user with the given
        username.
    """
    return User.nodes.get_or_none(username=user_name)
    
    
# ------------------------------------------------------------------------------
# CREATE USER
# ------------------------------------------------------------------------------
def create_user(account_data):
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
            email=email,
            is_active = True
        )

        # We set the password by calling the update function that handles
        # proper hashing of the password so we never store the actual
        # password

        user.update_password(password)
        return user

    except Exception as ex:
        # TODO Good exception handling!!!
        app.logger.error('An error building account occured: \n ' + str(ex))
        return None


# ------------------------------------------------------------------------------
# GET USER GROUPS
# ------------------------------------------------------------------------------
def get_user_groups(user_id):
    """
        Given a user id, gets the groups that the user belongs to. 
        
        :param user_id: The id of the user. 
        :return: A list of group names in uppercase. Empty list if user does
                 not belong to any group. 
    """
    user = get_user_by_id(user_id=user_id)
    groups = []
    if user is not None:
        for group in user.groups.all():
            groups.append(group.name.upper())
    return groups


# ------------------------------------------------------------------------------
# CREATE GROUP
# ------------------------------------------------------------------------------        
def create_group(group_data):
        """
        """
        # Run validations
        if 'name' not in group_data:
            return None
        if 'description' not in group_data:
            return None
        group = Group(
                group_id=str(uuid.uuid4()),
                name=group_data['name'].upper(),
                description=group_data['description']
            )
        return group


# ------------------------------------------------------------------------------
# ADD USERT TO GROUP
# ------------------------------------------------------------------------------
def add_user_to_group(caller_id, group_name, user):
    """
        Links a user to a given group
    """
    try:
        admins = Group.nodes.get_or_none(name="system")
        caller = User.nodes.get_or_none(user_id=caller_id)
        
        # We need to check that caller is member of admin in order to perform 
        # this action
        if admins is not None and caller is not None and caller.groups.is_connected(admins):
            user = User.nodes.get_or_none(user_id=user)
            group = User.nodes.get_or_none(name=group_name)
            if user is not None and group is not None and not user.groups.is_connected(group) and not group.members.is_connected(user):
                # (GROUP)-[HAS]->[USER]
                group.members.connect(user)
                group.save()
                # (USER)-[IS_MEMBER_OF]->(GROUP)
                user.groups.connect(group)
                user.save()
                return True
        return False
    except Exception as ex:
        # TODO - Do good exception handling here
        app.logger.error("Error adding user to group: \n " + str(ex))
        return False
""


# ------------------------------------------------------------------------------
# REQUIRES ROLES
# ------------------------------------------------------------------------------
def requires_roles(*roles):
    """
        TODO
        :param roles: 
        :return: 
    """
    def wrapper(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            if get_user_groups(current_user.user_id) not in roles:
                return render_template("error/401.html")
            return f(*args, **kwargs)
        return wrapped
    return wrapper


