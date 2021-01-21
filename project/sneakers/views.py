#################
#### imports ####
#################
 
from flask import render_template, Blueprint, request, redirect, url_for, flash
from project import db
from project.models import Sneaker
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
def index():
    all_sneaker = Sneaker.query.all()
    return render_template('sneakers.html', sneakers=all_sneaker)

@sneakers_blueprint.route('/add', methods=['GET', 'POST'])
def add_sneaker():
    form = AddSneakerForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            new_sneaker = Sneaker(form.sneaker_model_name.data, form.sneaker_retail_price.data)
            db.session.add(new_sneaker)
            db.session.commit()
            flash('New sneaker, {}, added!'.format(new_sneaker.sneaker_model_name), 'success')
            return redirect(url_for('sneakers.index'))
        else:
            flash_errors(form)
            flash('ERROR! Sneaker was not added.', 'error')

    return render_template('add_sneaker.html', form=form)



