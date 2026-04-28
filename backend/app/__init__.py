"""Application factory for the Supply Chain Flask backend."""
from datetime import datetime

from flask import Flask

from app.config import Config
from app.extensions import cors, mongo
from app.routes import suppliers, manufacturers, distributors, inventory, orders, logistics, dashboard


def _auto_seed():
    """Seed database with sample data if empty."""
    try:
        db = mongo.db

        # Check if already seeded
        if db.suppliers.count_documents({}) > 0:
            return

        print("🌱 Database empty — auto-seeding sample data...")

        # ========== 1. SUPPLIERS ==========
        supplier_data = [
            {"name": "Stark Industries", "contact_person": "Tony Stark", "email": "tony@starkindustries.com", "phone": "+1-212-555-3000", "country": "USA", "reliability_rating": 10},
            {"name": "Hammer Tech Corp", "contact_person": "Justin Hammer", "email": "j.hammer@hammertech.com", "phone": "+1-415-555-0042", "country": "USA", "reliability_rating": 6},
            {"name": "Obadiah Arms Ltd", "contact_person": "Stane Okafor", "email": "stane@obiarms.com", "phone": "+44-20-5555-0099", "country": "UK", "reliability_rating": 7},
            {"name": "SHIELD Procurement", "contact_person": "Nick Fury", "email": "n.fury@shield.gov", "phone": "+1-800-555-7447", "country": "USA", "reliability_rating": 9},
            {"name": "Wakanda Vibranium Co", "contact_person": "Shuri Udaku", "email": "shuri@wakanda.wk", "phone": "+27-11-555-0071", "country": "Wakanda", "reliability_rating": 10},
            {"name": "Wayne Enterprises", "contact_person": "Bruce Wayne", "email": "bruce@wayne.com", "phone": "+1-555-0010", "country": "USA", "reliability_rating": 8},
            {"name": "LexCorp Industries", "contact_person": "Lex Luthor", "email": "lex@lexcorp.com", "phone": "+1-555-0020", "country": "USA", "reliability_rating": 4},
            {"name": "Oscorp Industries", "contact_person": "Norman Osborn", "email": "norman@oscorp.com", "phone": "+1-555-0030", "country": "USA", "reliability_rating": 5},
            {"name": "AIM Advanced Ideas", "contact_person": "Aldrich Killian", "email": "aldrich@aim.com", "phone": "+1-555-0040", "country": "USA", "reliability_rating": 3},
            {"name": "Pym Technologies", "contact_person": "Hank Pym", "email": "hank@pymtech.com", "phone": "+1-555-0050", "country": "USA", "reliability_rating": 8},
        ]

        supplier_ids = db.suppliers.insert_many(supplier_data).inserted_ids
        print(f"   • {len(supplier_ids)} suppliers")
        supplier_map = {i + 1: sid for i, sid in enumerate(supplier_ids)}

        # ========== 2. MANUFACTURERS ==========
        manufacturer_data = [
            {"name": "Stark Malibu Forge", "location": "Malibu, USA", "capacity_per_day": 9000, "production_type": "Armor Systems", "supplier_id": supplier_map[1], "status": "active"},
            {"name": "Hammer Drone Plant", "location": "Queens, USA", "capacity_per_day": 4500, "production_type": "Drone Assembly", "supplier_id": supplier_map[2], "status": "active"},
            {"name": "Obadiah Heavy Works", "location": "London, UK", "capacity_per_day": 3000, "production_type": "Heavy Machinery", "supplier_id": supplier_map[3], "status": "maintenance"},
            {"name": "SHIELD Tech Facility", "location": "Helicarrier, Atlantic", "capacity_per_day": 2500, "production_type": "Defense Electronics", "supplier_id": supplier_map[4], "status": "active"},
            {"name": "Shuri Advanced Lab", "location": "Wakanda Central", "capacity_per_day": 15000, "production_type": "Vibranium Tech", "supplier_id": supplier_map[5], "status": "active"},
            {"name": "Wayne Applied Sciences", "location": "Gotham, USA", "capacity_per_day": 7000, "production_type": "Advanced Materials", "supplier_id": supplier_map[6], "status": "active"},
            {"name": "LexCorp R&D", "location": "Metropolis, USA", "capacity_per_day": 5000, "production_type": "Power Generation", "supplier_id": supplier_map[7], "status": "maintenance"},
            {"name": "Oscorp Bio-Lab", "location": "New York, USA", "capacity_per_day": 3500, "production_type": "Bio-Tech", "supplier_id": supplier_map[8], "status": "active"},
            {"name": "AIM Extremis Facility", "location": "Miami, USA", "capacity_per_day": 4000, "production_type": "Bio-Engineering", "supplier_id": supplier_map[9], "status": "idle"},
            {"name": "Pym Particle Labs", "location": "San Francisco, USA", "capacity_per_day": 6000, "production_type": "Nano-Tech", "supplier_id": supplier_map[10], "status": "active"},
        ]

        manufacturer_ids = db.manufacturers.insert_many(manufacturer_data).inserted_ids
        print(f"   • {len(manufacturer_ids)} manufacturers")
        manufacturer_map = {i + 1: mid for i, mid in enumerate(manufacturer_ids)}

        # ========== 3. DISTRIBUTORS ==========
        distributor_data = [
            {"name": "Avengers Express", "region": "North America", "warehouse_count": 18, "max_load_tons": 1200, "delivery_sla_days": 1},
            {"name": "Extremis Freight", "region": "Europe", "warehouse_count": 20, "max_load_tons": 900, "delivery_sla_days": 2},
            {"name": "SHIELD Air Cargo", "region": "Global", "warehouse_count": 8, "max_load_tons": 600, "delivery_sla_days": 1},
            {"name": "Stark Quinjet Courier", "region": "Asia Pacific", "warehouse_count": 14, "max_load_tons": 800, "delivery_sla_days": 2},
            {"name": "Iron Logistics Corp", "region": "South America", "warehouse_count": 10, "max_load_tons": 400, "delivery_sla_days": 3},
            {"name": "Wayne Freight Systems", "region": "North America", "warehouse_count": 22, "max_load_tons": 1500, "delivery_sla_days": 2},
            {"name": "LexCorp Distribution", "region": "Europe", "warehouse_count": 15, "max_load_tons": 1100, "delivery_sla_days": 3},
            {"name": "Oscorp Logistics", "region": "Asia Pacific", "warehouse_count": 12, "max_load_tons": 750, "delivery_sla_days": 2},
            {"name": "AIM Rapid Transport", "region": "Africa", "warehouse_count": 8, "max_load_tons": 500, "delivery_sla_days": 1},
            {"name": "Pym Micro-Delivery", "region": "Global", "warehouse_count": 30, "max_load_tons": 300, "delivery_sla_days": 1},
        ]

        distributor_ids = db.distributors.insert_many(distributor_data).inserted_ids
        print(f"   • {len(distributor_ids)} distributors")
        distributor_map = {i + 1: did for i, did in enumerate(distributor_ids)}

        # ========== 4. INVENTORY ==========
        inventory_data = [
            {"product_name": "Mark L Nanoparticle Core", "sku": "MK50-NPC", "category": "Armor Systems", "current_stock": 450, "reorder_point": 200, "max_capacity": 2000, "unit_cost": 980.00, "manufacturer_id": manufacturer_map[1]},
            {"product_name": "Repulsor Emitter Array", "sku": "REP-EM3", "category": "Weapons Tech", "current_stock": 80, "reorder_point": 150, "max_capacity": 1000, "unit_cost": 1450.00, "manufacturer_id": manufacturer_map[1]},
            {"product_name": "Arc Reactor Mini MkIII", "sku": "ARC-MK3", "category": "Power Systems", "current_stock": 3200, "reorder_point": 500, "max_capacity": 5000, "unit_cost": 2200.00, "manufacturer_id": manufacturer_map[1]},
            {"product_name": "Vibranium Alloy Plate", "sku": "VIB-AP10", "category": "Raw Material", "current_stock": 60, "reorder_point": 100, "max_capacity": 500, "unit_cost": 8800.00, "manufacturer_id": manufacturer_map[5]},
            {"product_name": "Hammer Drone CPU", "sku": "HD-CPU7", "category": "Drone Assembly", "current_stock": 310, "reorder_point": 200, "max_capacity": 1500, "unit_cost": 320.00, "manufacturer_id": manufacturer_map[2]},
            {"product_name": "HUD Holographic Chip", "sku": "HUD-HC9", "category": "Electronics", "current_stock": 95, "reorder_point": 300, "max_capacity": 3000, "unit_cost": 540.00, "manufacturer_id": manufacturer_map[4]},
            {"product_name": "Titanium-Gold Alloy Rod", "sku": "TGA-50MM", "category": "Raw Material", "current_stock": 720, "reorder_point": 100, "max_capacity": 2000, "unit_cost": 420.00, "manufacturer_id": manufacturer_map[3]},
            {"product_name": "JARVIS Neural Module", "sku": "JRV-NM2", "category": "AI Systems", "current_stock": 180, "reorder_point": 400, "max_capacity": 4000, "unit_cost": 6600.00, "manufacturer_id": manufacturer_map[1]},
            {"product_name": "Servo Actuator MkV", "sku": "SRV-MK5", "category": "Armor Systems", "current_stock": 25, "reorder_point": 50, "max_capacity": 500, "unit_cost": 1200.00, "manufacturer_id": manufacturer_map[1]},
            {"product_name": "Extremis Vial Set", "sku": "EXT-VS1", "category": "Bio-Tech", "current_stock": 1800, "reorder_point": 500, "max_capacity": 5000, "unit_cost": 88.00, "manufacturer_id": manufacturer_map[2]},
        ]

        inventory_ids = db.inventory.insert_many(inventory_data).inserted_ids
        print(f"   • {len(inventory_ids)} inventory items")
        inventory_map = {i + 1: iid for i, iid in enumerate(inventory_ids)}

        # ========== 5. ORDERS ==========
        order_data = [
            {"supplier_id": supplier_map[1], "inventory_id": inventory_map[1], "quantity": 500, "unit_price": 960.00, "status": "delivered", "priority": "high", "expected_delivery": datetime(2024, 1, 15)},
            {"supplier_id": supplier_map[2], "inventory_id": inventory_map[5], "quantity": 200, "unit_price": 310.00, "status": "processing", "priority": "critical", "expected_delivery": datetime(2024, 2, 1)},
            {"supplier_id": supplier_map[4], "inventory_id": inventory_map[6], "quantity": 1000, "unit_price": 520.00, "status": "shipped", "priority": "medium", "expected_delivery": datetime(2024, 1, 28)},
            {"supplier_id": supplier_map[5], "inventory_id": inventory_map[4], "quantity": 100, "unit_price": 8600.00, "status": "pending", "priority": "high", "expected_delivery": datetime(2024, 2, 10)},
            {"supplier_id": supplier_map[3], "inventory_id": inventory_map[7], "quantity": 300, "unit_price": 410.00, "status": "delivered", "priority": "medium", "expected_delivery": datetime(2024, 1, 20)},
            {"supplier_id": supplier_map[1], "inventory_id": inventory_map[8], "quantity": 800, "unit_price": 6500.00, "status": "pending", "priority": "critical", "expected_delivery": datetime(2024, 2, 5)},
            {"supplier_id": supplier_map[2], "inventory_id": inventory_map[10], "quantity": 500, "unit_price": 85.00, "status": "processing", "priority": "low", "expected_delivery": datetime(2024, 2, 8)},
            {"supplier_id": supplier_map[4], "inventory_id": inventory_map[6], "quantity": 600, "unit_price": 510.00, "status": "shipped", "priority": "medium", "expected_delivery": datetime(2024, 1, 30)},
            {"supplier_id": supplier_map[1], "inventory_id": inventory_map[9], "quantity": 100, "unit_price": 1180.00, "status": "pending", "priority": "high", "expected_delivery": datetime(2024, 2, 12)},
            {"supplier_id": supplier_map[3], "inventory_id": inventory_map[7], "quantity": 2000, "unit_price": 400.00, "status": "delivered", "priority": "low", "expected_delivery": datetime(2024, 1, 18)},
        ]

        order_ids = db.orders.insert_many(order_data).inserted_ids
        print(f"   • {len(order_ids)} orders")
        order_map = {i + 1: oid for i, oid in enumerate(order_ids)}

        # ========== 6. LOGISTICS ==========
        logistics_data = [
            {"order_id": order_map[1], "distributor_id": distributor_map[1], "carrier": "Stark Quinjet", "tracking_number": "STK-20240115-001", "origin": "Malibu", "destination": "New York", "shipping_cost": 850, "mode_of_transport": "air", "shipment_status": "delivered"},
            {"order_id": order_map[2], "distributor_id": distributor_map[3], "carrier": "SHIELD Helicarrier", "tracking_number": "SHL-20240201-002", "origin": "Queens", "destination": "Washington DC", "shipping_cost": 2200, "mode_of_transport": "air", "shipment_status": "in_transit"},
            {"order_id": order_map[3], "distributor_id": distributor_map[4], "carrier": "Iron Logistics Corp", "tracking_number": "ILC-20240128-003", "origin": "Helicarrier", "destination": "Tokyo", "shipping_cost": 3400, "mode_of_transport": "air", "shipment_status": "shipped"},
            {"order_id": order_map[5], "distributor_id": distributor_map[2], "carrier": "Extremis Freight", "tracking_number": "EXT-20240120-005", "origin": "London", "destination": "Berlin", "shipping_cost": 1800, "mode_of_transport": "road", "shipment_status": "delivered"},
            {"order_id": order_map[7], "distributor_id": distributor_map[1], "carrier": "Avengers Express", "tracking_number": "AVX-20240208-007", "origin": "Queens", "destination": "Los Angeles", "shipping_cost": 1100, "mode_of_transport": "road", "shipment_status": "in_transit"},
            {"order_id": order_map[8], "distributor_id": distributor_map[4], "carrier": "Stark Quinjet", "tracking_number": "STK-20240130-008", "origin": "Helicarrier", "destination": "Seoul", "shipping_cost": 2900, "mode_of_transport": "air", "shipment_status": "shipped"},
            {"order_id": order_map[10], "distributor_id": distributor_map[5], "carrier": "Iron Logistics Corp", "tracking_number": "ILC-20240118-010", "origin": "London", "destination": "Rio de Janeiro", "shipping_cost": 4200, "mode_of_transport": "sea", "shipment_status": "delivered"},
            {"order_id": order_map[4], "distributor_id": distributor_map[2], "carrier": "Extremis Freight", "tracking_number": "EXT-20240210-011", "origin": "Wakanda", "destination": "London", "shipping_cost": 2500, "mode_of_transport": "air", "shipment_status": "in_transit"},
            {"order_id": order_map[6], "distributor_id": distributor_map[5], "carrier": "Iron Logistics Corp", "tracking_number": "ILC-20240205-012", "origin": "Malibu", "destination": "Boston", "shipping_cost": 1500, "mode_of_transport": "road", "shipment_status": "pending"},
            {"order_id": order_map[9], "distributor_id": distributor_map[3], "carrier": "SHIELD Air Cargo", "tracking_number": "SHL-20240212-013", "origin": "New York", "destination": "Chicago", "shipping_cost": 1200, "mode_of_transport": "air", "shipment_status": "pending"},
        ]

        logistics_ids = db.logistics.insert_many(logistics_data).inserted_ids
        print(f"   • {len(logistics_ids)} logistics records")

        print("🎉 Auto-seeding complete!")

    except Exception as e:
        print(f"⚠️  Auto-seeding skipped: {e}")


def create_app(config_class=Config):
    """Application factory pattern."""
    app = Flask(__name__)
    app.config.from_object(config_class)
    app.url_map.strict_slashes = False  # Match Express behavior

    # Initialize extensions
    cors.init_app(app)
    mongo.init_app(app)

    # Auto-seed if database is empty
    _auto_seed()

    # Register blueprints
    app.register_blueprint(suppliers.bp, url_prefix='/api/suppliers')
    app.register_blueprint(manufacturers.bp, url_prefix='/api/manufacturers')
    app.register_blueprint(distributors.bp, url_prefix='/api/distributors')
    app.register_blueprint(inventory.bp, url_prefix='/api/inventory')
    app.register_blueprint(orders.bp, url_prefix='/api/orders')
    app.register_blueprint(logistics.bp, url_prefix='/api/logistics')
    app.register_blueprint(dashboard.bp, url_prefix='/api/dashboard')

    @app.route('/')
    def health_check():
        return {'message': '\U0001f69a Supply Chain MVC API Running on port 5000'}

    @app.errorhandler(Exception)
    def handle_exception(error):
        """Global error handler."""
        import traceback
        traceback.print_exc()
        response = {'success': False, 'error': str(error)}
        status_code = getattr(error, 'code', 500)
        return response, status_code

    return app
