import uuid
from thrive import app, login_manager
from thrive.models.graph import Student, LegalGuardian
from thrive.models.transactions import add_legal_guardian
from thrive.security.iam import requires_roles
from flask_login import login_user, login_required, current_user
from flask import jsonify, request, render_template


# --------------------------------------------------------------------------
# GET: /STUDENT
# --------------------------------------------------------------------------
@app.route('/student/<student_id>/legal_guardian/add', methods=['GET'])
@login_required
@requires_roles('STUDENT_ADMIN', 'SYS_ADMIN', 'TEACHERS', 'DIRECTORS')
def get_create_legal_guardian(student_id):
    try:
        student = Student.nodes.get_or_none(student_id)
        if student is not None:
            render_template("")
        else:
            return render_template("error/404", err="Error de al conectarse a la base de datos")
    except Exception as ex:
        print(ex)
        return render_template("error/404", err="Error de al conectarse a la base de datos")
