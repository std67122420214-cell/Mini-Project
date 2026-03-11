import os
from flask import Flask
from formulaone.extensions import db, login_manager, bcrypt
from formulaone.models import User, Team, FormulaOne
from formulaone.core.routes import core_bp
from formulaone.users.routes import users_bp
from formulaone.formulaone.routes import formulaone_bp

def create_app():
  app = Flask(__name__)
  app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
  app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')

  db.init_app(app)
  bcrypt.init_app(app)
  login_manager.init_app(app)
  login_manager.login_view = 'users.login'
  login_manager.login_message = 'Please login before access this page!'
  login_manager.login_message_category = 'warning'

  app.register_blueprint(core_bp, url_prefix='/')
  app.register_blueprint(users_bp, url_prefix='/users')
  app.register_blueprint(formulaone_bp, url_prefix='/formulaones')
  
  return app