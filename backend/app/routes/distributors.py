"""Distributor routes."""
from datetime import datetime
from flask import Blueprint, request, jsonify

from app.extensions import mongo
from app.utils import serialize_doc

bp = Blueprint('distributors', __name__)


@bp.route('/', methods=['GET'])
def get_distributors():
    distributors = list(mongo.db.distributors.find().sort('created_at', -1))
    return jsonify(serialize_doc(distributors))


@bp.route('/', methods=['POST'])
def create_distributor():
    data = request.get_json()
    data['created_at'] = datetime.utcnow()
    result = mongo.db.distributors.insert_one(data)
    created = mongo.db.distributors.find_one({'_id': result.inserted_id})
    return jsonify(serialize_doc(created)), 201
