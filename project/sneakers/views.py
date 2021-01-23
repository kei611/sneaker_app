#################
#### imports ####
#################
 
from flask import render_template, Blueprint, request, redirect, url_for, flash
from flask_login import current_user, login_required
from werkzeug.utils import secure_filename
import os

from project import db, app
from project.models import Sneaker, User
from .forms import AddSneakerForm

 
################
#### config ####
################
 
sneakers_blueprint = Blueprint('sneakers', __name__)
 
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
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

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

 
################
#### routes ####
################
 
@sneakers_blueprint.route('/')
def public_sneakers():
    all_public_sneakers = Sneaker.query.filter_by(is_public=True)
    return render_template('public_sneakers.html', public_sneakers=all_public_sneakers)


@sneakers_blueprint.route('/add', methods=['GET', 'POST'])
def add_sneaker():
    # Cannot pass in 'request.form' to AddRecipeForm constructor, as this will cause 'request.files' to not be
    # sent to the form.  This will cause AddRecipeForm to not see the file data.
    # Flask-WTF handles passing form data to the form, so not parameters need to be included.
    form = AddSneakerForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            # check if the post request has the recipe_image part
            if 'sneaker_image' not in request.files:
                flash('No sneaker image provided!')
                return redirect(request.url)

            file = request.files['sneaker_image']

            if file.filename == '':
                flash('No selected file')
                return redirect(request.url)

            if not file:
                flash('File is empty!')
                return redirect(request.url)

            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filepath = os.path.join(app.config['UPLOADS_DEFAULT_DEST'], filename)
                file.save(filepath)
                url = os.path.join(app.config['UPLOADS_DEFAULT_URL'], filename)
            else:
                filename = ''
                url = ''

            name = form.sneaker_model_name.data
            price = form.sneaker_retail_price.data

            new_sneaker = Sneaker(name, price, current_user.id, True, None, filename, url)
            
            db.session.add(new_sneaker)
            db.session.commit()
            flash('New sneaker, {}, added!'.format(new_sneaker.sneaker_model_name), 'success')
            return redirect(url_for('sneakers.user_sneakers'))
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