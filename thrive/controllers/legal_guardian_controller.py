import uuid
from thrive import app, login_manager
from thrive.models.graph import Student, LegalGuardian
from thrive.models.transactions import add_legal_guardian
from thrive.security.iam import requires_roles
from flask_login import login_user, login_required, current_user
from flask import jsonify, request, render_template, redirect, url_for



# --------------------------------------------------------------------------
# GET: /STUDENT
# --------------------------------------------------------------------------
@app.route('/student/<student_id>/legal_guardian/add', methods=['GET'])
@login_required
@requires_roles('STUDENT_ADMIN', 'SYS_ADMIN', 'TEACHERS', 'DIRECTORS')
def get_create_legal_guardian(student_id):
    try:
        student = Student.nodes.get_or_none(student_id=student_id)
        if student is not None:
            return render_template("legal_guardian/add.html", student_id=student_id)
        else:
            return render_template("error/404", err="El identificador de estudiante no es válido")
    except Exception as ex:
        print(ex)
        return render_template("error/404", err="Error de al conectarse a la base de datos")


# --------------------------------------------------------------------------
# POST: /STUDENT
# --------------------------------------------------------------------------
@app.route('/student/<student_id>/legal_guardian/add', methods=['POST'])
@login_required
@requires_roles('STUDENT_ADMIN', 'SYS_ADMIN', 'TEACHERS', 'DIRECTORS')
def post_create_legal_guardian(student_id):
    try:
        student = Student.nodes.get_or_none(student_id=student_id)
        if student is not None:
            print('readign stuff....')
            guardian = LegalGuardian(
                personal_id = request.form['personal-id'],
                name = request.form['name'],
                last_name = request.form['last-name'],
                second_last_name = request.form['second-last-name'],
                phone_number = request.form['phone-number'],
                email = request.form['email'],
                address = request.form['address']
            )
            add_legal_guardian(student=student, legal_guardian=guardian)
            return redirect(url_for('get_student',student_id=student.student_id ))
            
        else:
            return render_template("error/404", err="El identificador de estudiante no es válido")
    except Exception as ex:
        print(ex)
        return render_template("error/404", err="Error de al conectarse a la base de datos")