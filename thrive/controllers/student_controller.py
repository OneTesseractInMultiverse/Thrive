"""
from thrive import app
from thrive.models.graph import Student
from flask_login import login_user, login_required
from flask import jsonify, request, render_template


# ==========================================================================
# GETTERS
# ==========================================================================

# --------------------------------------------------------------------------
# GET: /COURSE/CREATE
# --------------------------------------------------------------------------
@app.route('/student/add', methods=['GET'])
def get_add_student():
    return render_template("student/add.html")


# --------------------------------------------------------------------------
# GET: /COURSE
# --------------------------------------------------------------------------
@app.route('/student/add', methods=['POST'])
def post_add_student():

    for key, value in request.form.items():
        print('key: ' + key + " [value=" + value + "]")
    print("Creating student...")
    try:
        student = Student(
            personal_id=request.form['personal-id'],
            name=request.form['name'],
            last_name=request.form['last-name'],
            second_last_name=request.form['second-last-name'],
            birth_day=request.form['birth-day'],
            birth_motnh=request.form['birth-month'],
            birth_year=request.form['birth-year']
        )
        print("Student created...Now Saving...")
        student.save()
    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        print(message)

    return jsonify({"msg": "Shit got real..."})
"""