"""Order routes."""
from datetime import datetime
from flask import Blueprint, request, jsonify
from bson import ObjectId

from app.extensions import mongo
from app.utils import serialize_doc

bp = Blueprint('orders', __name__)


def _populate_order_refs(orders):
    for o in orders:
        if o.get('supplier_id'):
            sup = mongo.db.suppliers.find_one(
                {'_id': ObjectId(o['supplier_id'])}, {'name': 1}
            )
            if sup:
                o['supplier_id'] = {
                    '_id': str(sup['_id']),
                    'name': sup.get('name'),
                }
        if o.get('inventory_id'):
            inv = mongo.db.inventory.find_one(
                {'_id': ObjectId(o['inventory_id'])},
                {'product_name': 1, 'sku': 1},
            )
            if inv:
                o['inventory_id'] = {
                    '_id': str(inv['_id']),
                    'product_name': inv.get('product_name'),
                    'sku': inv.get('sku'),
                }
    return orders


@bp.route('/', methods=['GET'])
def get_orders():
    orders = list(mongo.db.orders.find().sort('order_date', -1))
    orders = _populate_order_refs(orders)
    return jsonify(serialize_doc(orders))


@bp.route('/', methods=['POST'])
def create_order():
    data = request.get_json()
    data['order_date'] = datetime.utcnow()
    result = mongo.db.orders.insert_one(data)
    created = mongo.db.orders.find_one({'_id': result.inserted_id})
    return jsonify(serialize_doc(created)), 201
