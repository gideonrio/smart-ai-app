from flask import Blueprint, jsonify, request

store_bp = Blueprint('store', __name__)


@store_bp.route('/store', methods=['GET'])
def get_store():
    products = [
        {
            "id": 1,
            "name": "Urea Fertilizer (50 Kg)",
            "category": "Fertilizer",
            "description": "High-quality Nitrogen fertilizer. Best for paddy, wheat, sugarcane.",
            "price": 280,
            "mrp": 340,
            "rating": 4.5,
            "amazon_link": "https://www.amazon.in/s?k=urea+fertilizer+50kg",
            "icon": "fa-leaf"
        },
        {
            "id": 2,
            "name": "DAP (Di-Ammonium Phosphate) 50Kg",
            "category": "Fertilizer",
            "description": "Provides Nitrogen & Phosphorus. Essential for root development and early growth.",
            "price": 1350,
            "mrp": 1500,
            "rating": 4.7,
            "amazon_link": "https://www.amazon.in/s?k=DAP+fertilizer+50kg",
            "icon": "fa-seedling"
        },
        {
            "id": 3,
            "name": "Neem Oil Pesticide (1 L)",
            "category": "Pesticide",
            "description": "100% organic neem oil. Effective against aphids, whitefly, mealybugs.",
            "price": 320,
            "mrp": 450,
            "rating": 4.6,
            "amazon_link": "https://www.amazon.in/s?k=neem+oil+pesticide+agriculture",
            "icon": "fa-flask"
        },
        {
            "id": 4,
            "name": "Chlorpyrifos 20% EC (1 L)",
            "category": "Pesticide",
            "description": "Broad spectrum insecticide for soil & foliar pests.",
            "price": 410,
            "mrp": 550,
            "rating": 4.2,
            "amazon_link": "https://www.amazon.in/s?k=chlorpyrifos+20+EC",
            "icon": "fa-bug"
        },
        {
            "id": 5,
            "name": "Drip Irrigation Kit (1 Acre)",
            "category": "Equipment",
            "description": "Complete drip system. Saves 50% water. Easy to install.",
            "price": 3800,
            "mrp": 5200,
            "rating": 4.8,
            "amazon_link": "https://www.amazon.in/s?k=drip+irrigation+kit+1+acre",
            "icon": "fa-tint"
        },
        {
            "id": 6,
            "name": "Mancozeb 75% WP Fungicide (500g)",
            "category": "Fungicide",
            "description": "Controls early blight, late blight, downy mildew in crops.",
            "price": 185,
            "mrp": 240,
            "rating": 4.4,
            "amazon_link": "https://www.amazon.in/s?k=mancozeb+75+WP+fungicide",
            "icon": "fa-shield-virus"
        },
        {
            "id": 7,
            "name": "Vermi Compost (25 Kg)",
            "category": "Organic",
            "description": "100% natural organic compost. Improves soil fertility and structure.",
            "price": 180,
            "mrp": 250,
            "rating": 4.9,
            "amazon_link": "https://www.amazon.in/s?k=vermi+compost+25kg+agriculture",
            "icon": "fa-recycle"
        },
        {
            "id": 8,
            "name": "Hand Sprayer Pump 16L",
            "category": "Equipment",
            "description": "Agricultural battery-operated knapsack sprayer. 16 Litre capacity.",
            "price": 1100,
            "mrp": 1650,
            "rating": 4.3,
            "amazon_link": "https://www.amazon.in/s?k=battery+knapsack+sprayer+16L+agriculture",
            "icon": "fa-spray-can"
        }
    ]

    category = request.args.get('category', None)
    if category and category != 'All':
        products = [p for p in products if p['category'] == category]

    return jsonify(products), 200
