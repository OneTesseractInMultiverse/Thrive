import uuid
from thrive import app, login_manager
from thrive.models.graph import Student
from thrive.security.iam import requires_roles
from flask_login import login_user, login_required, current_user
from flask import jsonify, request, render_template


# ==========================================================================
# VIEW STUDENT
# ==========================================================================

# --------------------------------------------------------------------------
# GET: /STUDENT
# --------------------------------------------------------------------------
@app.route('/student/<student_id>', methods=['GET'])
@login_required
@requires_roles('STUDENT_ADMIN', 'SYS_ADMIN', 'TEACHERS', 'DIRECTORS')
def get_student(student_id):
    try:
        student = Student.nodes.get_or_none(student_id)
        if student is not None:
            render_template("")
    except Exception as ex:
        print(ex)
        return render_template("error/404", err="Error de al conectarse a la base de datos")


# ==========================================================================
# ADD STUDENT
# ==========================================================================


# --------------------------------------------------------------------------
# GET: /STUDENT/ADD
# --------------------------------------------------------------------------
@app.route('/student/add', methods=['GET'])
@login_required
@requires_roles('STUDENT_ADMIN', 'SYS_ADMIN')
def get_add_student():
    return render_template("student/add.html")


# --------------------------------------------------------------------------
# POST: /STUDENT/ADD
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
            education_level=request.form['education-level'],
            education_level_year=request.form['education-level-year'],
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
