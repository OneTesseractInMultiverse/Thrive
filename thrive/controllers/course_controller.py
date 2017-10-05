from thrive import app
from thrive.models.course import Course
from flask_login import login_user, login_required
from flask import jsonify, request, render_template


# ==========================================================================
# GETTERS
# ==========================================================================

# --------------------------------------------------------------------------
# GET: /COURSE
# --------------------------------------------------------------------------
@app.route('/course/<level>', methods=['GET'])
@login_required
def get_courses(level):
    """
        Gest the complete list of all active courses in the system. It only 
        displays the active courses in a given level. Each course has an 
        specific level.
    """

    return jsonify({"msg": "To be implemented"})
    
    
# --------------------------------------------------------------------------
# GET: /COURSE/<COURSE_ID>
# --------------------------------------------------------------------------
@app.route('/course/<course_id>', methods=['GET'])
@login_required
def get_course(course_id):
    """
    """

    return jsonify({"msg": "To be implemented"})


# --------------------------------------------------------------------------
# GET: /COURSE/CREATE
# --------------------------------------------------------------------------
@app.route('/course/add', methods=['GET'])
@login_required
def get_add_course():
    """
    """
    return jsonify({"msg": "To be implemented"})


# --------------------------------------------------------------------------
# GET: /COURSE/<COURSE_ID>/UPDATE
# --------------------------------------------------------------------------
@app.route('/course/<course_id>/update', methods=['GET'])
@login_required
def get_update_course():
    """
    """
    return jsonify({"msg": "To be implemented"})


# ==========================================================================
# POSTERS
# ==========================================================================

# --------------------------------------------------------------------------
# GET: /COURSE
# --------------------------------------------------------------------------
@app.route('/course/add', methods=['POST'])
@login_required
def post_add_course():
    """
        Gest the complete list of all active courses in the system. It only 
        displays the active courses in a given level. Each course has an 
        specific level.
    """

    return jsonify({"msg": "To be implemented"})