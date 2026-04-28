"""Manufacturer routes."""
from datetime import datetime
from flask import Blueprint, request, jsonify
from bson import ObjectId

from app.extensions import mongo
from app.utils import serialize_doc

bp = Blueprint('manufacturers', __name__)


def _populate_supplier(manufacturers):
    for m in manufacturers:
        if m.get('supplier_id'):
            supplier = mongo.db.suppliers.find_one(
                {'_id': ObjectId(m['supplier_id'])}, {'name': 1}
            )
            if supplier:
                m['supplier_id'] = {
                    '_id': str(supplier['_id']),
                    'name': supplier.get('name'),
                }
    return manufacturers


@bp.route('/', methods=['GET'])
def get_manufacturers():
    manufacturers = list(mongo.db.manufacturers.find().sort('created_at', -1))
    manufacturers = _populate_supplier(manufacturers)
    return jsonify(serialize_doc(manufacturers))


@bp.route('/', methods=['POST'])
def create_manufacturer():
    data = request.get_json()
    data['created_at'] = datetime.utcnow()
    result = mongo.db.manufacturers.insert_one(data)
    created = mongo.db.manufacturers.find_one({'_id': result.inserted_id})
    return jsonify(serialize_doc(created)), 201
