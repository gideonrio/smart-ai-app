from flask import Blueprint, jsonify

satellite_monitor_bp = Blueprint('satellite_monitor', __name__)


@satellite_monitor_bp.route('/satellite-data', methods=['GET'])
def get_satellite_data():
    # Mock Google Earth Engine / Sentinel data
    return jsonify({
        "ndvi_index": 0.72,
        "crop_health_status": "Good",
        "stress_areas": "North-East corner shows low moisture.",
        "growth_stage": "Vegetative"
    }), 200
