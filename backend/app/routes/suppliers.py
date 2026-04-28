"""Supplier routes."""
from datetime import datetime
from flask import Blueprint, request, jsonify

from app.extensions import mongo
from app.utils import serialize_doc

bp = Blueprint('suppliers', __name__)


@bp.route('/', methods=['GET'])
def get_suppliers():
    suppliers = list(mongo.db.suppliers.find().sort('created_at', -1))
    return jsonify(serialize_doc(suppliers))


@bp.route('/', methods=['POST'])
def create_supplier():
    data = request.get_json()
    data['created_at'] = datetime.utcnow()
    result = mongo.db.suppliers.insert_one(data)
    created = mongo.db.suppliers.find_one({'_id': result.inserted_id})
    return jsonify(serialize_doc(created)), 201
