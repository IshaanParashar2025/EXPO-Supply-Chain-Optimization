"""Dashboard analytics routes."""
from flask import Blueprint, jsonify
from bson import ObjectId

from app.extensions import mongo
from app.utils import serialize_doc

bp = Blueprint('dashboard', __name__)


def _populate_order_fields(orders):
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


@bp.route('/stats', methods=['GET'])
def get_stats():
    return jsonify({
        'suppliers': mongo.db.suppliers.count_documents({}),
        'manufacturers': mongo.db.manufacturers.count_documents({}),
        'inventory': mongo.db.inventory.count_documents({}),
        'orders': mongo.db.orders.count_documents({
            'status': {'$nin': ['delivered', 'cancelled']}
        }),
        'lowStock': mongo.db.inventory.count_documents({
            '$expr': {'$lte': ['$current_stock', '$reorder_point']}
        }),
    })


@bp.route('/alerts', methods=['GET'])
def get_alerts():
    critical_orders = mongo.db.orders.count_documents({
        'priority': 'critical', 'status': 'pending'
    })
    low_items = list(mongo.db.inventory.find(
        {'$expr': {'$lte': ['$current_stock', '$reorder_point']}},
        sort=[('current_stock', 1)],
        limit=5,
    ))
    return jsonify({
        'criticalOrders': critical_orders,
        'lowItems': serialize_doc(low_items),
    })


@bp.route('/inventory-by-category', methods=['GET'])
def get_inventory_by_category():
    pipeline = [
        {'$group': {'_id': '$category', 'total': {'$sum': '$current_stock'}}},
        {'$sort': {'total': -1}},
    ]
    cats = list(mongo.db.inventory.aggregate(pipeline))
    return jsonify(serialize_doc(cats))


@bp.route('/recent-orders', methods=['GET'])
def get_recent_orders():
    orders = list(mongo.db.orders.find(sort=[('order_date', -1)], limit=8))
    orders = _populate_order_fields(orders)
    return jsonify(serialize_doc(orders))


@bp.route('/optimization', methods=['GET'])
def get_optimization():
    replenishment = list(mongo.db.inventory.find(
        {'$expr': {'$lte': ['$current_stock', '$reorder_point']}},
        sort=[('current_stock', 1)],
        limit=10,
    ))

    stockout_risk = list(mongo.db.inventory.find(
        {'$expr': {'$lte': ['$current_stock', {
            '$multiply': ['$reorder_point', 0.5]
        }]}},
        sort=[('current_stock', 1)],
    ))

    transport = list(mongo.db.logistics.aggregate([
        {'$group': {
            '_id': '$mode_of_transport',
            'count': {'$sum': 1},
            'avgCost': {'$avg': '$shipping_cost'},
            'totalCost': {'$sum': '$shipping_cost'},
        }},
        {'$sort': {'totalCost': -1}},
    ]))

    fulfillment = list(mongo.db.orders.aggregate([
        {'$group': {
            '_id': '$status',
            'count': {'$sum': 1},
            'totalValue': {'$sum': {'$multiply': ['$quantity', '$unit_price']}},
        }},
        {'$sort': {'count': -1}},
    ]))

    supplier_perf = list(mongo.db.suppliers.aggregate([
        {'$lookup': {
            'from': 'orders',
            'localField': '_id',
            'foreignField': 'supplier_id',
            'as': 'orders',
        }},
        {'$project': {
            'name': 1,
            'country': 1,
            'reliability_rating': 1,
            'orderCount': {'$size': '$orders'},
            'score': {'$multiply': [{'$size': '$orders'}, '$reliability_rating']},
        }},
        {'$sort': {'score': -1}},
    ]))

    return jsonify(serialize_doc({
        'replenishment': replenishment,
        'stockoutRisk': stockout_risk,
        'transport': transport,
        'fulfillment': fulfillment,
        'supplierPerf': supplier_perf,
    }))
