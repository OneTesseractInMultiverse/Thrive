import uuid
from thrive import app
from thrive.models.graph import Group
from thrive.security.iam import (
    create_group,
    sys_add_user_to_group,
    find_group
)
from flask import jsonify, request
from flask_jwt_extended import jwt_required


# --------------------------------------------------------------------------
# POST GROUP
# --------------------------------------------------------------------------
@app.route('/api/v1/group', methods=['POST'])
def post_group():
    """
        Creates persistent definitions of a an access group. This groups are 
        used to define the structures that produce the identity and access
        management infrastructure.
    """
    # First we verify the request is an actual json request. If not, then we
    # responded with a HTTP 400 Bad Request result code.
    if not request.is_json:
        app.logger.warning('Request without JSON payload received on token endpoint')
        return jsonify({"msg": "Only JSON request is supported"}), 400

    # If we get here, is because the request contains valid json so we can
    # parse the parameters
    group_data = request.get_json()

    if 'name' not in group_data or 'description' not in group_data:
        return jsonify({
            "msg": "Name or description is not present in payload"
        }), 400

    group = create_group(group_data)
    group.save()
    return jsonify({
        "group_id": group.group_id,
        "name": group.name,
        "description": group.description
    }), 201


# --------------------------------------------------------------------------
# POST GROUP MEMBER
# --------------------------------------------------------------------------
@app.route('/api/v1/group/<group_id>/member', methods=['POST'])
def post_group_member(group_id):
    # First we verify the request is an actual json request. If not, then we
    # responded with a HTTP 400 Bad Request result code.
    if not request.is_json:
        app.logger.warning('Request without JSON payload received on token endpoint')
        return jsonify({"msg": "Only JSON request is supported"}), 400

    # If we get here, is because the request contains valid json so we can
    # parse the parameters
    assoc_data = request.get_json()

    if 'user_id' not in assoc_data:
        return jsonify({
            "msg": "You must provide a valid user id for this operation"
        }), 400

    if sys_add_user_to_group(group_id=group_id, user_id=assoc_data['user_id']):
        return jsonify({
            "msg":"User was successfully added to group"
        }), 201
    return jsonify({
        "msg": "The add_user_to_group transaction could not be completed. Verify the user id is valid"
    }), 400


# --------------------------------------------------------------------------
# GET GROUP BY ID
# --------------------------------------------------------------------------
@app.route('/api/v1/group/<group_id>', methods=['GET'])
def get_group(group_id):
    """
        Given a group_id identifier, finds the associated group instances and
        return a json representation of the group. 
        
        :param group_id: The id of the group
        :return: Json representation of the group
    """
    group = find_group(group_id)
    if group is None:
        return jsonify({
            "msg": "The requested group could not be found"
        }), 404
    return jsonify({
        "group_id": group.group_id,
        "name": group.name,
        "description": group.description
    }), 200



