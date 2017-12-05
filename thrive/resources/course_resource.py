import uuid
from flask import jsonify, request
from thrive import app
from thrive.models.graph import Course
from thrive.security.iam import create_course
from thrive.models.transactions import add_student_to_course

# --------------------------------------------------------------------------
# POST COURSE
# --------------------------------------------------------------------------
@app.route('/api/v1/course', methods=['POST'])
def post_course():
    # First we verify the request is an actual json request. If not, then we
    # responded with a HTTP 400 Bad Request result code.
    if not request.is_json:
        app.logger.warning('Request without JSON payload received on token endpoint')
        return jsonify({"msg": "Only JSON request is supported"}), 400
        
    # If we get here, is because the request contains valid json so we can
    # parse the parameters
    course_data = request.get_json()
    
    if not('title' not in course_data and 'description' not in course_data and 'education_level_year' not in course_data and 'year' not in course_data):
        return jsonify({
                "msg": "Title or description or year or educational level is not present in payload"    
            }), 400
    
    course = create_course(course_data)
    course.save()
    return jsonify({
        "course_id": course.course_id,
        "title": course.title,
        "description": course.description,
        "year": course.year,
        "education_level_year": course.education_level_year
    }),201