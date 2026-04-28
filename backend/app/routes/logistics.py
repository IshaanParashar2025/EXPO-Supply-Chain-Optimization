"""Logistics routes."""
from datetime import datetime
from flask import Blueprint, request, jsonify
from bson import ObjectId

from app.database import get_db
from app.utils import serialize_doc

bp = Blueprint('logistics', __name__)


def _populate_logistics_refs(logistics):
    db = get_db()
    for l in logistics:
        if l.get('order_id'):
            order = db.orders.find_one(
                {'_id': ObjectId(l['order_id'])}, {'supplier_id': 1}
            )
            if order:
                l['order_id'] = {
                    '_id': str(order['_id']),
                    'supplier_id': str(order.get('supplier_id')),
                }
        if l.get('distributor_id'):
            dist = db.distributors.find_one(
                {'_id': ObjectId(l['distributor_id'])}, {'name': 1}
            )
            if dist:
                l['distributor_id'] = {
                    '_id': str(dist['_id']),
                    'name': dist.get('name'),
                }
    return logistics


@bp.route('/', methods=['GET'])
def get_logistics():
    db = get_db()
    logistics = list(db.logistics.find().sort('created_at', -1))
    logistics = _populate_logistics_refs(logistics)
    return jsonify(serialize_doc(logistics))


@bp.route('/', methods=['POST'])
def create_logistics():
    db = get_db()
    data = request.get_json()
    data['created_at'] = datetime.utcnow()
    result = db.logistics.insert_one(data)
    created = db.logistics.find_one({'_id': result.inserted_id})
    return jsonify(serialize_doc(created)), 201

