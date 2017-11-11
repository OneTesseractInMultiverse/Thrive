import uuid
from thrive import app, login_manager
from thrive.models.graph import Student
from thrive.security.iam import requires_roles
from flask_login import login_user, login_required, current_user
from flask import jsonify, request, render_template


# ==========================================================================
# GETTERS
# ==========================================================================

# --------------------------------------------------------------------------
# GET: /COURSE/CREATE
# --------------------------------------------------------------------------
@app.route('/student/add', methods=['GET'])
@login_required
@requires_roles('STUDENT_ADMIN', 'SYS_ADMIN')
def get_add_student():
    return render_template("student/add.html")


# --------------------------------------------------------------------------
# GET: /COURSE
# --------------------------------------------------------------------------
@app.route('/student/add', methods=['POST'])
@login_required
@requires_roles('STUDENT_ADMIN', 'SYS_ADMIN')
def post_add_student():
    try:
        student = Student(
            student_id=str(uuid.uuid4()),
            personal_id=request.form['personal-id'],
            name=request.form['name'],
            last_name=request.form['last-name'],
            second_last_name=request.form['second-last-name'],
            active=True
        )
        student.set_date_of_birth(
            day=int(request.form['birth-day']),
            month=int(request.form['birth-month']),
            year=int(request.form['birth-year'])
        )
        student.save()
    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        app.logger.error(message)
        return render_template("student/add.html", err="Debe completar todos los campos requeridos", form=request.form)

    return jsonify({"msg": "Shit got real..."})
