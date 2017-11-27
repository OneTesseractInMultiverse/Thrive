from thrive import app
from thrive.models.stats import (
    count_total_students,
    count_total_active_students,
    count_total_teachers,
    count_total_users
)
from flask_login import login_user, login_required
from flask import jsonify, request, render_template


# --------------------------------------------------------------------------
# GET: /ACCOUNT
# --------------------------------------------------------------------------
@app.route('/', methods=['GET'])
@login_required
def get_dashboard_root():
    """
        Gets the main application dashboard view if the user is already 
        authenticated.
        :return: Status response json
    """
    t_students = count_total_students()
    t_active_studs = count_total_active_students()
    t_teachers = count_total_teachers()
    t_users = count_total_users()
    return render_template(
        "dashboard/index.html",
        t_students=t_students,
        t_active_studs=t_active_studs,
        t_teachers=t_teachers,
        t_users=t_users
    )
    
    

