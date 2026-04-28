"""Inventory routes."""
from datetime import datetime
from flask import Blueprint, request, jsonify
from bson import ObjectId

from app.database import get_db
from app.utils import serialize_doc

bp = Blueprint('inventory', __name__)


def _populate_manufacturer(items):
    db = get_db()
    for item in items:
        if item.get('manufacturer_id'):
            man = db.manufacturers.find_one(
                {'_id': ObjectId(item['manufacturer_id'])}, {'name': 1}
            )
            if man:
                item['manufacturer_id'] = {
                    '_id': str(man['_id']),
                    'name': man.get('name'),
                }
    return items


@bp.route('/', methods=['GET'])
def get_inventory():
    db = get_db()
    items = list(db.inventory.find().sort('last_updated', -1))
    items = _populate_manufacturer(items)
    return jsonify(serialize_doc(items))


@bp.route('/', methods=['POST'])
def create_inventory():
    db = get_db()
    data = request.get_json()
    data['last_updated'] = datetime.utcnow()
    result = db.inventory.insert_one(data)
    created = db.inventory.find_one({'_id': result.inserted_id})
    return jsonify(serialize_doc(created)), 201

