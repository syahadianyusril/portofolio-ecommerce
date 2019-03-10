import logging, json
from flask import Blueprint
from flask_restful import Api, Resource, reqparse, marshal
from blueprints import db
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, get_jwt_claims

from . import *

bp_user = Blueprint('client', __name__)
api = Api(bp_user)

class AdminResource(Resource):

    def __init__(self):
        pass

    @jwt_required
    def get(self, id = None):
        if id == None :
            if(get_jwt_claims()['status'] == "admin"):
                parser = reqparse.RequestParser()
                parser.add_argument('p', type=int, location='args', default=1)
                parser.add_argument('rp', type=int, location='args', default=999)
                args = parser.parse_args()

                offset = (args['p'] * args['rp']) - args['rp']

                qry_all = Users.query

                list_get_all = []

                for data in qry_all.limit(args['rp']).offset(offset).all() :
                    list_get_all.append(marshal(data, Users.response_field))
                return list_get_all, 200, {'Content-Type':'application/json'}
            return {"Message" : "Only admin is allowed"},404, {'Content-Type':'application/json'}

        else :
            qry_id = Users.query.get(id)
            if qry_id != None :
                return marshal(qry_id, Users.response_field), 200, {'Content-Type':'application/json'}
            return {'Message': 'Data Not Found'}, 404, {'Content-Type':'application/json'}
        return {'Message': 'Data Not Match'}, 404, {'Content-Type':'application/json'}
    
    # belom
    @jwt_required
    def put(self, id):
        if(get_jwt_claims()['status'] == "admin") or (get_jwt_claims()['id'] == id):
            parser = reqparse.RequestParser()
            parser.add_argument('name', location='json')
            parser.add_argument('email', location='json')
            parser.add_argument('phone_number', location='json')
            parser.add_argument('daerah', location='json')
            parser.add_argument('username', location='json')
            parser.add_argument('password', location='json')
            args = parser.parse_args()

            qry_put = Users.query.get(id)
            if qry_put != None :
                qry_put.name = args['name']
                qry_put.email = args['email']
                qry_put.phone_number = args['phone_number']
                qry_put.daerah = args['daerah']
                qry_put.username = args['username']
                qry_put.password = args['password']
                db.session.commit()
                return marshal(qry_put, Users.response_field), 200, {'Content-Type':'application/json'}
            return {'Message': 'Data Not Found'}, 404, {'Content-Type':'application/json'}
        return {'Message': 'Authentication Failed'}, 404, {'Content-Type':'application/json'}
        
    @jwt_required   
    def delete(self, id):
        if(get_jwt_claims()['status'] == "admin") or (get_jwt_claims()['id'] == id) :
            qry_delete = Users.query.get(id)
            if qry_delete != None :
                db.session.delete(qry_delete)
                db.session.commit()
                return {'Status' : 'Delete Completed'}, 200, {'Content-Type':'application/json'}
            return {'Status': 'Delete Uncompleted', 'Message' : 'Data Not Found'}, 404, {'Content-Type':'application/json'}
        return {'Message' : 'Authentication Failed'}, 404, {'Content-Type':'application/json'}
    
  
    @jwt_required
    def post(self):
        if(get_jwt_claims()['status'] != "admin"):
            return {"message" : "Only admin is allowed"},404, {'Content-Type':'application/json'}
        parser = reqparse.RequestParser()
        parser.add_argument('name', location='json', required=True)
        parser.add_argument('email', location='json', required=True)
        parser.add_argument('phone_number', location='json', required=True)
        parser.add_argument('daerah', location='json', required=True)
        parser.add_argument('username', location='json', required=True)
        parser.add_argument('password', location='json', required=True)
        parser.add_argument('status', location='json', required=True)
        args = parser.parse_args()
        print(args)
        
        list_client = Users(None, args['name'], args['email'], args['phone_number'], args['daerah'], args['username'], args['password'], args['status'])
        db.session.add(list_client)
        db.session.commit()

        return marshal(list_client, Users.response_field), 200, {'Content-Type':'application/json'}

class RegisterResource(Resource):

    def __init__(self):
        pass
    
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', location='json', required=True)
        parser.add_argument('email', location='json', required=True)
        parser.add_argument('phone_number', location='json', required=True)
        parser.add_argument('daerah', location='json', required=True)
        parser.add_argument('username', location='json', required=True)
        parser.add_argument('password', location='json', required=True)
        args = parser.parse_args()
        
        list_user_reg = Users(None, args['name'], args['email'], args['phone_number'], args['daerah'], args['username'], args['password'], "penjual")
        db.session.add(list_user_reg)
        db.session.commit()

        return {'Message':'Regiter Success'}, 200, {'Content-Type':'application/json'}

class LoginResource(Resource):

    def __init__(self):
        pass
    
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', location='json', required=True)
        parser.add_argument('password', location='json', required=True)
        args = parser.parse_args()
        
        qry = Users.query.filter_by(username=args['username']).filter_by(password=args['password']).first()
        if qry != None :
            token = create_access_token(marshal(qry, Users.response_field))
        else : 
            return {'status':'UNAUTHORIZED', 'message':'invalid username or password'}, 401
        return {'token': token}, 200

api.add_resource(AdminResource, '/users', '/user/<int:id>')
api.add_resource(LoginResource, '/user/login')
api.add_resource(RegisterResource, '/user/register')