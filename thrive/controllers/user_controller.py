from flask import render_template, redirect, url_for
from flask import request, session
from flask_login import login_user, logout_user, login_required

from thrive import app, login_manager
from thrive.security.iam import get_user_by_username


@login_manager.unauthorized_handler
def unauthorized():
    return redirect(url_for('get_account_login'))


# --------------------------------------------------------------------------
# GET /LOGIN
# --------------------------------------------------------------------------
# Root resource
@app.route('/login', methods=['GET'])
def get_account_login():
    return render_template("authentication/login.html")


# --------------------------------------------------------------------------
# POST /LOGIN
# --------------------------------------------------------------------------
# Root resource
@app.route('/login', methods=['POST'])
def post_account_login():
    """
        First we need to verify the request contains a username and a password
        if not, then we must display an error.
        :return:
    """
    app.logger.info('Reading credentials from request...')
    username = request.form['username']
    password = request.form['password']

    if username is None:
        return render_template("authentication/login.html", error="Debe proporcionar un usuario")
    if password is None:
        return render_template("authentication/login.html", error="Debe proporcionar una contrasena")

    app.logger.info('Credentials OK, now authenticating...')

    user = get_user_by_username(username)
    if user is None:
        return render_template("authentication/login.html", error="No se ha encontrado el usuario proporcionado")

    if user.authenticate(password):
        app.logger.info('Credentials are correct...')
        session['logged_in'] = True
        login_user(user)
        return redirect(url_for('get_dashboard_root'))
    else:
        app.logger.info('Credentials are not correct...')
        error = "Wrong username or password!"
        return render_template("authentication/login.html", error=error)


# --------------------------------------------------------------------------
# POST /LOGOUT
# --------------------------------------------------------------------------
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('get_account_login'))
