#################
#### imports ####
#################
 
from flask import render_template, Blueprint, request, redirect, url_for, flash
from flask_login import current_user, login_required
from project import db
from project.models import Sneaker, User
from .forms import AddSneakerForm

 
################
#### config ####
################
 
sneakers_blueprint = Blueprint('sneakers', __name__)
 
##########################
#### helper functions ####
##########################

def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ), 'info')

 
################
#### routes ####
################
 
@sneakers_blueprint.route('/')
def public_sneakers():
    all_public_sneakers = Sneaker.query.filter_by(is_public=True)
    return render_template('public_sneakers.html', public_sneakers=all_public_sneakers)


@sneakers_blueprint.route('/add', methods=['GET', 'POST'])
def add_sneaker():
    form = AddSneakerForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            new_sneaker = Sneaker(form.sneaker_model_name.data, form.sneaker_retail_price.data, current_user.id, True)
            db.session.add(new_sneaker)
            db.session.commit()
            flash('New sneaker, {}, added!'.format(new_sneaker.sneaker_model_name), 'success')
            return redirect(url_for('sneakers.public_sneakers'))
        else:
            flash_errors(form)
            flash('ERROR! Sneaker was not added.', 'error')

    return render_template('add_sneaker.html', form=form)


@sneakers_blueprint.route('/sneakers')
@login_required
def user_sneakers():
    all_user_sneakers = Sneaker.query.filter_by(user_id=current_user.id)
    return render_template('user_sneakers.html', user_sneakers=all_user_sneakers)


@sneakers_blueprint.route('/sneaker/<sneaker_id>')
def sneaker_details(sneaker_id):
    sneaker_with_user = db.session.query(Sneaker, User).join(User).filter(Sneaker.id == sneaker_id).first()
    if sneaker_with_user is not None:
        if sneaker_with_user.Sneaker.is_public:
            return render_template('sneaker_detail.html', sneaker=sneaker_with_user)
        else:
            if current_user.is_authenticated and sneaker_with_user.Sneaker.user_id == current_user.id:
                return render_template('sneaker_detail.html', sneaker=sneaker_with_user)
            else:
                flash('Error! Incorrect permissions to access this sneaker.', 'error')
    else:
        flash('Error! Sneaker does not exist.', 'error')
    return redirect(url_for('sneakers.public_sneakers'))