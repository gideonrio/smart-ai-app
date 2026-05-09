from flask import Blueprint, request, jsonify

seasonal_planning_bp = Blueprint('seasonal_planning', __name__)

# Data patterns for crop suggestions
SEASONAL_DATA = {
    "summer": {
        "sandy": ["Watermelon", "Cucumber", "Groundnut"],
        "clay": ["Cotton", "Maize", "Sorghum"],
        "loamy": ["Sugar Beet", "Sunflower", "Millets"]
    },
    "winter": {
        "sandy": ["Carrots", "Potato", "Radish"],
        "clay": ["Wheat", "Chickpea", "Mustard"],
        "loamy": ["Tomato", "Cabbage", "Peas"]
    },
    "monsoon": {
        "sandy": ["Pearl Millet", "Cowpea"],
        "clay": ["Rice", "Soybean", "Sugarcane"],
        "loamy": ["Brinjal", "Chillies", "Pulse crops"]
    }
}

CROP_DETAILS = {
    "Watermelon": {"profit": "₹80,000 - ₹1.2L", "water": "Medium", "cycle": "90 days"},
    "Cucumber": {"profit": "₹50,000 - ₹90,000", "water": "High", "cycle": "60 days"},
    "Groundnut": {"profit": "₹60,000 - ₹1L", "water": "Low", "cycle": "110 days"},
    "Cotton": {"profit": "₹1.5L - ₹2.5L", "water": "High", "cycle": "160 days"},
    "Maize": {"profit": "₹70,000 - ₹1.1L", "water": "Medium", "cycle": "100 days"},
    "Rice": {"profit": "₹1.2L - ₹2L", "water": "Very High", "cycle": "120 days"},
    "Wheat": {"profit": "₹90,000 - ₹1.4L", "water": "Medium", "cycle": "130 days"},
    "Tomato": {"profit": "₹1L - ₹3L", "water": "Medium", "cycle": "100 days"},
    "Sugarcane": {"profit": "₹2L - ₹4L", "water": "High", "cycle": "300+ days"}
}


@seasonal_planning_bp.route('/seasonal-plan', methods=['POST'])
def get_seasonal_plan():
    data = request.get_json()
    location = data.get('location', 'Tamil Nadu')
    soil = data.get('soil', 'loamy').lower()
    season = data.get('season', 'summer').lower()

    # Suggest crops
    suggested_crops = SEASONAL_DATA.get(season, SEASONAL_DATA['summer']).get(
        soil, SEASONAL_DATA['summer']['loamy'])

    plans = []
    for crop in suggested_crops:
        details = CROP_DETAILS.get(
            crop, {"profit": "Varies", "water": "Regular", "cycle": "100 days"})
        plans.append({
            "crop": crop,
            "profit": details["profit"],
            "water_needs": details["water"],
            "cycle": details["cycle"],
            "reason": f"Best suited for {soil} soil in {season} at {location}."
        })

    return jsonify({
        "location": location,
        "soil": soil.title(),
        "season": season.title(),
        "plans": plans
    }), 200

# Crop Timeline Tracker Data


@seasonal_planning_bp.route('/crop-timeline', methods=['GET'])
def get_crop_timeline():
    # Mock data for a typical crop growth
    return jsonify({
        "crop": "Tomato",
        "current_week": 4,
        "timeline": [
            {"week": 1, "icon": "🌱", "status": "Good",
                "desc": "Seeds sprouted successfully"},
            {"week": 2, "icon": "🌿", "status": "Healthy",
                "desc": "Formation of secondary leaves"},
            {"week": 3, "icon": "🌼", "status": "Normal",
                "desc": "Flower buds appearing"},
            {"week": 4, "icon": "🍅", "status": "Ready soon",
                "desc": "Fruits are turning red"},
            {"week": 5, "icon": "🏁", "status": "Upcoming",
                "desc": "Final harvesting phase"}
        ]
    }), 200
