#################
#### imports ####
#################
 
from flask import render_template, Blueprint, request, redirect, flash, url_for
from sqlalchemy.exc import IntegrityError

from project import db
from project.models import User
from.forms import RegisterForm
 
################
#### config ####
################
 
users_blueprint = Blueprint('users', __name__)
 
 
################
#### routes ####
################
 
@users_blueprint.route('/login')
def login():
    return render_template('login.html')

@users_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            try:
                new_user = User(form.email.data, form.password.data)
                new_user.authenticated = True
                db.session.add(new_user)
                db.session.commit()
                flash('Thanks for registering!', 'success')
                return redirect(url_for('sneakers.index'))
            except IntegrityError:
                db.session.rollback()
                flash('ERROR! Email ({}) already exists.'.format(form.email.data), 'error')
    return render_template('register.html', form=form)
