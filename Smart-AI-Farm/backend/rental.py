from flask import Blueprint, jsonify, request

rental_bp = Blueprint('rental', __name__)

REAL_SHOPS = [
    {
        "id": "real_1",
        "name": "Mahindra 575 DI Tractor",
        "type": "Tractor",
        "price": "₹600/hr",
        "owner_name": "JFarm Services (TAFE), Chennai",
        "phone": "+919840098400",
        "rating": 4.8,
        "image": "fa-tractor",
        "color": "#e67e22",
        "lat": 13.0827,
        "lon": 80.2707
    },
    {
        "id": "real_2",
        "name": "Sonalika Harvester Combine",
        "type": "Harvester",
        "price": "₹1500/hr",
        "owner_name": "KhetiGaadi Rentals, Pune",
        "phone": "+919021114111",
        "rating": 4.6,
        "image": "fa-truck",
        "color": "#2ecc71",
        "lat": 18.5204,
        "lon": 73.8567
    },
    {
        "id": "real_3",
        "name": "AgriBot Spraying Drone",
        "type": "Drone",
        "price": "₹1200/hr",
        "owner_name": "Kisan Drones Pvt Ltd, Bangalore",
        "phone": "+918073004000",
        "rating": 4.9,
        "image": "fa-helicopter",
        "color": "#3498db",
        "lat": 12.9716,
        "lon": 77.5946
    },
    {
        "id": "real_4",
        "name": "Rotavator & Heavy Ploughs",
        "type": "Implement",
        "price": "₹400/hr",
        "owner_name": "Farmkart Solutions, Bhopal",
        "phone": "+918826688266",
        "rating": 4.5,
        "image": "fa-cogs",
        "color": "#9b59b6",
        "lat": 23.2599,
        "lon": 77.4126
    },
    {
        "id": "real_5",
        "name": "John Deere 5050 D Tractor",
        "type": "Tractor",
        "price": "₹750/hr",
        "owner_name": "EM3 AgriServices, New Delhi",
        "phone": "+919999111222",
        "rating": 4.7,
        "image": "fa-tractor",
        "color": "#e67e22",
        "lat": 28.6139,
        "lon": 77.2090
    }
]


def calc_dist(lat1, lon1, lat2, lon2):
    try:
        return round(((float(lat1) - float(lat2))**2 + (float(lon1) - float(lon2))**2)**0.5 * 111, 1)
    except:
        return 0


@rental_bp.route('/equipments', methods=['GET'])
def get_equipment():
    lat = request.args.get('lat')
    lon = request.args.get('lon')

    results = []
    for shop in REAL_SHOPS:
        dist = calc_dist(lat, lon, shop['lat'],
                         shop['lon']) if lat and lon else 0
        dist_str = f" ({dist} km away)" if dist > 0 else ""

        results.append({
            "id": shop["id"],
            "name": shop["name"],
            "type": shop["type"],
            "price": shop["price"],
            "owner": f"{shop['owner_name']}{dist_str}",
            "phone": shop["phone"],
            "rating": shop["rating"],
            "image": shop["image"],
            "color": shop["color"],
            "lat": shop["lat"],
            "lon": shop["lon"]
        })

    # Sort by nearest if lat/lon provided
    if lat and lon:
        results = sorted(results, key=lambda x: calc_dist(
            lat, lon, x['lat'], x['lon']))

    return jsonify(results)
