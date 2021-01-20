#################
#### imports ####
#################
 
from flask import Flask
 
 
################
#### config ####
################
 
app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile('flask.cfg')
 
 
####################
#### blueprints ####
####################
 
from project.users.views import users_blueprint
from project.sneakers.views import sneakers_blueprint
 
# register the blueprints
app.register_blueprint(users_blueprint)
app.register_blueprint(sneakers_blueprint)