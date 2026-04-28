"""Logistics / shipment routes."""
from datetime import datetime
from flask import Blueprint, request, jsonify
from bson import ObjectId

from app.extensions import mongo
from app.utils import serialize_doc

bp = Blueprint('logistics', __name__)


def _populate_logistics_refs(items):
    for item in items:
        if item.get('order_id'):
            order = mongo.db.orders.find_one(
                {'_id': ObjectId(item['order_id'])},
                {'supplier_id': 1, 'inventory_id': 1},
            )
            if order:
                item['order_id'] = {
                    '_id': str(order['_id']),
                }
        if item.get('distributor_id'):
            dist = mongo.db.distributors.find_one(
                {'_id': ObjectId(item['distributor_id'])}, {'name': 1}
            )
            if dist:
                item['distributor_id'] = {
                    '_id': str(dist['_id']),
                    'name': dist.get('name'),
                }
    return items


@bp.route('/', methods=['GET'])
def get_logistics():
    items = list(mongo.db.logistics.find().sort('created_at', -1))
    items = _populate_logistics_refs(items)
    return jsonify(serialize_doc(items))


@bp.route('/', methods=['POST'])
def create_logistics():
    data = request.get_json()
    data['created_at'] = datetime.utcnow()
    result = mongo.db.logistics.insert_one(data)
    created = mongo.db.logistics.find_one({'_id': result.inserted_id})
    return jsonify(serialize_doc(created)), 201
