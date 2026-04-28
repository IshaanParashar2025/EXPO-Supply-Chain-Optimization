"""Distributor routes."""
from datetime import datetime
from flask import Blueprint, request, jsonify

from app.database import get_db
from app.utils import serialize_doc

bp = Blueprint('distributors', __name__)


@bp.route('/', methods=['GET'])
def get_distributors():
    db = get_db()
    distributors = list(db.distributors.find().sort('created_at', -1))
    return jsonify(serialize_doc(distributors))


@bp.route('/', methods=['POST'])
def create_distributor():
    db = get_db()
    data = request.get_json()
    data['created_at'] = datetime.utcnow()
    result = db.distributors.insert_one(data)
    created = db.distributors.find_one({'_id': result.inserted_id})
    return jsonify(serialize_doc(created)), 201

