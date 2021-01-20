#################
#### imports ####
#################
 
from flask import render_template, Blueprint
 
 
################
#### config ####
################
 
sneakers_blueprint = Blueprint('sneakers', __name__, template_folder='templates')
 
 
################
#### routes ####
################
 
@sneakers_blueprint.route('/')
def index():
    return render_template('index.html')