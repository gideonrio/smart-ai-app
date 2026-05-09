from flask import Blueprint, jsonify, request
from typing import Any, Dict, List

market_prices_bp = Blueprint('market_prices', __name__)


@market_prices_bp.route('/market-prices', methods=['GET'])
def get_market_prices():
    city = str(request.args.get('city', '')).lower()

    all_data: List[Dict[str, Any]] = [
        {"crop": "Tomato (தக்காளி)", "price": "45 ₹/kg", "trend": "Up",
         "market": "Chennai - Koyambedu", "variety": "Sivam", "is_local": False},
        {"crop": "Paddy (நெல்)", "price": "2,250 ₹/Quintal", "trend": "Stable",
         "market": "Madurai - Mattuthavani", "variety": "Ponni", "is_local": False},
        {"crop": "Turmeric (மஞ்சள்)", "price": "8,400 ₹/Quintal", "trend": "Up",
         "market": "Erode Market", "variety": "Finger (விரலி)", "is_local": False},
        {"crop": "Small Onion (சின்ன வெங்காயம்)", "price": "65 ₹/kg", "trend": "Up",
         "market": "Dindigul Market", "variety": "Bellary Local", "is_local": False},
        {"crop": "Onion (பெரிய வெங்காயம்)", "price": "35 ₹/kg", "trend": "Stable",
         "market": "Coimbatore - MGR Market", "variety": "Nasik", "is_local": False},
        {"crop": "Banana (வாழைப்பழம்)", "price": "450 ₹/Bunch", "trend": "Down",
         "market": "Trichy - Gandhi Market", "variety": "Poovan", "is_local": False},
        {"crop": "Cotton (பருத்தி)", "price": "7,200 ₹/Quintal", "trend": "Down",
         "market": "Coimbatore - Annur", "variety": "DCH-32", "is_local": False},
        {"crop": "Maize (சோளம்)", "price": "2,150 ₹/Quintal", "trend": "Stable",
         "market": "Salem Market", "variety": "Kaveri 50", "is_local": False},
        {"crop": "Groundnut (நிலக்கடலை)", "price": "88 ₹/kg", "trend": "Up",
         "market": "Vellore Market", "variety": "TMV-7", "is_local": False},
        {"crop": "Dry Chilli (மிளகாய் வற்றல்)", "price": "195 ₹/kg", "trend": "Down",
         "market": "Tuticorin Market", "variety": "Samba", "is_local": False},
        {"crop": "Coconut (தேங்காய்)", "price": "34 ₹/Piece", "trend": "Stable",
         "market": "Pollachi Market", "variety": "Grade A", "is_local": False},
        {"crop": "Black Gram (உளுந்து)", "price": "7,800 ₹/Quintal", "trend": "Up",
         "market": "Villupuram Market", "variety": "Vamban", "is_local": False},
        {"crop": "Green Gram (பாசிப்பயறு)", "price": "8,200 ₹/Quintal", "trend": "Stable",
         "market": "Thanjavur Market", "variety": "CO-8", "is_local": False},
        {"crop": "Jasmine (மல்லிகைப்பூ)", "price": "450 ₹/kg", "trend": "Up",
         "market": "Madurai Flower Market", "variety": "Mundu", "is_local": False},
        {"crop": "Sugarcane (கரும்பு)", "price": "2,900 ₹/Ton", "trend": "Stable",
         "market": "Govt Fixed FRP", "variety": "CO-86032", "is_local": False}
    ]

    # Simple logic: prioritize markets that mention the city name
    if city:
        def market_key(x: Dict[str, Any]) -> bool:
            m = str(x.get('market', '')).lower()
            return city in m

        sorted_data = sorted(all_data, key=market_key, reverse=True)
        # Tag the top ones as 'Local'
        for item in sorted_data:
            m_name = str(item.get('market', '')).lower()
            if city in m_name:
                item['is_local'] = True
        return jsonify(sorted_data), 200

    return jsonify(all_data), 200
