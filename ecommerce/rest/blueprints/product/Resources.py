import logging, json, datetime
from flask import Blueprint
from flask_restful import Api, Resource, reqparse, marshal
from blueprints import db
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, get_jwt_claims

from . import *

bp_product = Blueprint('product', __name__)
api = Api(bp_product)

class ProductsResource(Resource):

    def __init__(self):
        pass

    # @jwt_required
    def get(self, id = None):
        qry_all = Products.query
        if id == None :
            parser = reqparse.RequestParser()
            parser.add_argument('p', type=int, location='args', default=1)
            parser.add_argument('rp', type=int, location='args', default=999)
            parser.add_argument('search', type=str, location='args')
            args = parser.parse_args()
            offset = (args['p'] * args['rp']) - args['rp']
            
            if args['search'] is not None:
                qry_all = qry_all.filter(Products.merk.like("%"+args['search']+"%"))
                if qry_all.first() is None:
                    qry_all = Products.query.filter(Products.type.like("%"+args['search']+"%"))

            list_products = []

            for data in qry_all.limit(args['rp']).offset(offset).all() :
                list_products.append(marshal(data, Products.response_field))
                
            return list_products, 200, {'Content-Type':'application/json'}
        else :
            qry_id = Products.query.get(id)
            if qry_id != None :
                return marshal(qry_id, Products.response_field), 200, {'Content-Type':'application/json'}
            return {'Message': 'Data Not Found'}, 404, {'Content-Type':'application/json'}
    
    @jwt_required
    def put(self, id):
        qry_put = Products.query.get(id)
        if(get_jwt_claims()['status'] == "admin") or (get_jwt_claims()['username'] ==  qry_put.posted_by):
            parser = reqparse.RequestParser()
            parser.add_argument('merk', location='json', required=True)
            parser.add_argument('type', location='json', required=True)
            parser.add_argument('category', location='json', required=True)
            parser.add_argument('kondisi', location='json', required=True)
            parser.add_argument('garansi', location='json', required=True)
            parser.add_argument('processor', location='json', required=True)
            parser.add_argument('vga', location='json', required=True)
            parser.add_argument('ram', location='json', required=True)
            parser.add_argument('storage', location='json', required=True)
            parser.add_argument('monitor', location='json', required=True)
            parser.add_argument('kelengkapan', location='json', required=True)
            parser.add_argument('deskripsi', location='json', required=True)
            parser.add_argument('harga', location='json', required=True)
            args = parser.parse_args()

            if qry_put != None :
                qry_put.merk = args['merk']
                qry_put.type = args['type']
                qry_put.category = args['category']
                qry_put.kondisi = args['kondisi']
                qry_put.garansi = args['garansi']
                qry_put.processor = args['processor']
                qry_put.vga = args['vga']
                qry_put.ram = args['ram']
                qry_put.storage = args['storage']
                qry_put.monitor = args['monitor']
                qry_put.kelengkapan = args['kelengkapan']
                qry_put.deskripsi = args['deskripsi']
                qry_put.harga = args['harga']
                db.session.commit()
                return marshal(qry_put, Products.response_field), 200, {'Content-Type':'application/json'}
            return {'Message': 'Data Not Found'}, 404, {'Content-Type':'application/json'}
        return {'Message': 'Authentication Failed'}, 404, {'Content-Type':'application/json'}

    @jwt_required   
    def delete(self, id):
        qry_delete = Products.query.get(id)
        if(get_jwt_claims()['status'] == "admin") or (get_jwt_claims()['username'] ==  qry_delete.posted_by):
            if qry_delete != None :
                db.session.delete(qry_delete)
                db.session.commit()
                return {'Status' : 'Delete Completed'}, 200, {'Content-Type':'application/json'}
            return {'Status': 'Delete Uncompleted', 'Message' : 'Data Not Found'}, 404, {'Content-Type':'application/json'}
        return {'Message' : 'Authentication Failed'}, 404, {'Content-Type':'application/json'}
    
    @jwt_required
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('merk', location='json', required=True)
        parser.add_argument('type', location='json', required=True)
        parser.add_argument('category', location='json', required=True)
        parser.add_argument('kondisi', location='json', required=True)
        parser.add_argument('garansi', location='json', required=True)
        parser.add_argument('processor', location='json', required=True)
        parser.add_argument('vga', location='json', required=True)
        parser.add_argument('ram', location='json', required=True)
        parser.add_argument('storage', location='json', required=True)
        parser.add_argument('monitor', location='json', required=True)
        parser.add_argument('kelengkapan', location='json', required=True)
        parser.add_argument('deskripsi', location='json', required=True)
        parser.add_argument('harga', location='json', required=True)
        args = parser.parse_args()

        posted_at_full = datetime.datetime.now()
        posted_at = posted_at_full.strftime("%c")

        posted_by = (get_jwt_claims()['username'])

        list_products = Products(None, args['merk'], args['type'], args['category'], posted_at, posted_by, args['kondisi'], args['garansi'], args['processor'], args['vga'], args['ram'], args['storage'], args['monitor'], args['kelengkapan'], args['deskripsi'], args['harga'])
        db.session.add(list_products)
        db.session.commit()

        return marshal(list_products, Products.response_field), 200, {'Content-Type':'application/json'}

api.add_resource(ProductsResource, '/products', '/product/<int:id>')