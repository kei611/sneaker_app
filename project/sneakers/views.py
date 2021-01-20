#################
#### imports ####
#################
 
from flask import render_template, Blueprint
from project.models import Sneaker
 
################
#### config ####
################
 
sneakers_blueprint = Blueprint('sneakers', __name__, template_folder='templates')
 
 
################
#### routes ####
################
 
@sneakers_blueprint.route('/')
def index():
    all_sneaker = Sneaker.query.all()
    return render_template('sneakers.html', sneakers=all_sneaker)