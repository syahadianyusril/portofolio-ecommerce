#challange.py
from flask import Flask, request, url_for, Blueprint
from flask_restful import Resource, Api, reqparse, abort
import json, logging
from logging.handlers import RotatingFileHandler
from time import strftime
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_jwt_extended import JWTManager
from datetime import timedelta
app = Flask(__name__)
api = Api(app, catch_all_404s=True)

# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost:3306/ecommerce'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['JWT_SECRET_KEY'] = 'jagdja751Akqgwuequiwii12Akjwdkwq'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=1)
 
jwt = JWTManager(app)

@jwt.user_claims_loader
def add_claims_to_access_token(identity):
    return identity

db = SQLAlchemy(app)
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

@app.after_request
def after_request(response):
    if request.method=='GET':
        app.logger.warning("REQUEST_LOG\t%s%s", json.dumps({'request':request.args.to_dict(),'response':json.loads(response.data.decode('utf-8'))}), request.method)
    else:
        app.logger.warning("REQUEST_LOG\t%s", json.dumps({'request':request.get_json(),'response':json.loads(response.data.decode('utf-8'))}))        
    return response

# from blueprints.auth import bp_auth
from blueprints.user.Resources import bp_user
from blueprints.product.Resources import bp_product

# app.register_blueprint(bp_auth, url_prefix='/auth')
app.register_blueprint(bp_user)
app.register_blueprint(bp_product)

db.create_all()
