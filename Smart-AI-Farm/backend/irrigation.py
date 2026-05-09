from flask import Blueprint, request, jsonify
from datetime import datetime

irrigation_bp = Blueprint('irrigation', __name__)


def get_irrigation_recommendation(crop, soil_moisture, temperature, rain_prob, area_acres):
    """Smart irrigation logic based on inputs"""

    # Base water needs per crop (litres/acre/day)
    crop_water_needs = {
        "rice": 600, "wheat": 350, "maize": 400, "cotton": 450,
        "sugarcane": 700, "tomato": 300, "onion": 250, "potato": 320
    }

    base_need = crop_water_needs.get(crop.lower(), 350)

    # Adjust for temperature
    temp_factor = 1.0
    if temperature > 35:
        temp_factor = 1.3
    elif temperature > 30:
        temp_factor = 1.15
    elif temperature < 20:
        temp_factor = 0.85

    # Adjust for soil moisture
    moisture_factor = 1.0
    if soil_moisture < 30:
        moisture_factor = 1.4  # Very dry - needs more
    elif soil_moisture < 50:
        moisture_factor = 1.1
    elif soil_moisture > 70:
        moisture_factor = 0.5  # Already moist
    elif soil_moisture > 90:
        moisture_factor = 0.0  # No irrigation needed

    # Reduce if rain is expected
    rain_factor = 1.0
    if rain_prob > 70:
        rain_factor = 0.1  # Heavy rain coming - skip
    elif rain_prob > 40:
        rain_factor = 0.5  # Some rain - reduce

    water_litres = base_need * area_acres * \
        temp_factor * moisture_factor * rain_factor

    # Best time recommendation
    hour = datetime.now().hour
    if 5 <= hour < 9:
        best_time = "Now (Early morning is ideal!)"
        time_reason = "Early morning reduces evaporation by 30%"
    elif hour < 17:
        best_time = "Evening (after 6:00 PM)"
        time_reason = "Avoid midday irrigation - high evaporation loss"
    else:
        best_time = "Now or early tomorrow morning"
        time_reason = "Evening/morning irrigation is best for crop health"

    # Alert
    alert = None
    if rain_prob > 70:
        alert = "🌧️ Heavy rain expected! You can skip irrigation today."
    elif soil_moisture < 20:
        alert = "⚠️ Critical: Soil moisture very low! Irrigate immediately."
    elif soil_moisture > 85:
        alert = "✅ Soil moisture is good. No irrigation needed today."
    elif temperature > 40:
        alert = "🔥 Heatwave! Double your irrigation frequency."

    return {
        "water_litres": round(water_litres),
        "best_time": best_time,
        "time_reason": time_reason,
        "alert": alert,
        "skip_irrigation": water_litres < 50,
        "frequency": "Twice daily" if temperature > 38 else "Daily" if soil_moisture < 40 else "Every 2 days"
    }


@irrigation_bp.route('/irrigation', methods=['POST'])
def irrigation_recommend():
    data = request.get_json()
    crop = data.get('crop', 'wheat')
    soil_moisture = float(data.get('soil_moisture', 50))
    temperature = float(data.get('temperature', 30))
    rain_prob = float(data.get('rain_prob', 20))
    area_acres = float(data.get('area_acres', 1))

    result = get_irrigation_recommendation(
        crop, soil_moisture, temperature, rain_prob, area_acres)
    return jsonify(result), 200
