from thrive import app
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
    return render_template("dashboard/index.html")
    
    

