from flask import Blueprint, request, jsonify
from datetime import datetime, timedelta

calendar_bp = Blueprint('calendar', __name__)

CROP_CALENDAR = {
    "paddy": {
        "sowing_months": "June - July / Oct - Nov",
        "harvesting_months": "90-120 days after sowing",
        "duration_days": 120,
        "schedule": [
            {"day": 0, "task": "🌱 Nursery Sowing",
                "detail": "Prepare nursery beds using 25kg seeds per acre."},
            {"day": 25, "task": "🌿 Transplanting",
                "detail": "Transplant seedlings at 15x10 cm spacing. Maintain water."},
            {"day": 45, "task": "💊 First Top Dressing",
                "detail": "Apply Urea 30kg and MOP 15kg per acre."},
            {"day": 65, "task": "🚿 Active Tillering",
                "detail": "Maintain 5cm water level. Spray for Leaf Folder if needed."},
            {"day": 90, "task": "🌾 Flowering Stage",
                "detail": "Maintain constant water level. Watch for Grain Discoloration."},
            {"day": 120, "task": "🏁 Harvesting",
                "detail": "Harvest when 80-90% panicles turn golden brown."}
        ]
    },
    "sugarcane": {
        "sowing_months": "Feb - March / Dec - Jan",
        "harvesting_months": "10-12 months after planting",
        "duration_days": 330,
        "schedule": [
            {"day": 0, "task": "🌱 Planting Sets",
                "detail": "Plant 2-3 budded sets in furrows with 90cm spacing."},
            {"day": 30, "task": "💊 Basal Fertilizer",
                "detail": "Apply 30:20:25 kg NPK per acre."},
            {"day": 60, "task": "🌿 Germination Care",
                "detail": "Gap filling and first weeding. Ensure adequate moisture."},
            {"day": 120, "task": "🚀 Tillering Boost",
                "detail": "Apply Urea 50kg per acre. Earthing up operation."},
            {"day": 210, "task": "🏗️ Propping",
                "detail": "Tie canes to prevent lodging. Manage Shoot Borer if present."},
            {"day": 330, "task": "🏁 Harvesting",
                "detail": "Harvest at peak maturity (Brix > 20). Bottom cutting."}
        ]
    },
    "banana": {
        "sowing_months": "June - July / Feb - March",
        "harvesting_months": "11-13 months after planting",
        "duration_days": 360,
        "schedule": [
            {"day": 0, "task": "🌱 Pit Preparation",
                "detail": "Dig 0.6m pits and plant suckers/tissue culture plants."},
            {"day": 45, "task": "💊 Fertilization",
                "detail": "Apply 110g N, 35g P, 330g K per plant."},
            {"day": 90, "task": "🌿 Desuckering",
                "detail": "Remove unwanted side suckers to focus growth on main stem."},
            {"day": 180, "task": "🏗️ Support (Propping)",
             "detail": "Provide bamboo support as bunch weight increases."},
            {"day": 240, "task": "🍌 Bunch Covering",
                "detail": "Cover bunches with blue/perforated polythene for quality."},
            {"day": 360, "task": "🏁 Harvesting",
                "detail": "Harvest when fruits reach full maturity and ridges disappear."}
        ]
    },
    "coconut": {
        "sowing_months": "June - July / Oct - Nov",
        "harvesting_months": "Perennial (Monthly)",
        "duration_days": 365,
        "schedule": [
            {"day": 0, "task": "🌱 Basin Opening",
                "detail": "Open basins around the palm (1.8m radius)."},
            {"day": 30, "task": "💊 Organic Manure",
                "detail": "Apply 50kg FYM or Green manure per palm."},
            {"day": 60, "task": "🚿 Irrigation",
                "detail": "Drip irrigation: 30-45 liters per day per palm."},
            {"day": 120, "task": "🐛 Pest Check",
                "detail": "Watch for Rhinoceros beetle and Red palm weevil."},
            {"day": 240, "task": "💊 NPK Dose",
                "detail": "Apply 1.3kg Urea, 2kg Super Phosphate, 2kg MOP."},
            {"day": 365, "task": "🏁 Harvest Cycle",
                "detail": "Harvest nuts every 30-45 days. Check for nut maturity."}
        ]
    },
    "groundnut": {
        "sowing_months": "Jan - Feb / June - July",
        "harvesting_months": "100-110 days after sowing",
        "duration_days": 105,
        "schedule": [
            {"day": 0, "task": "🌱 Sowing",
                "detail": "Treat seeds with Trichoderma. Sow at 30x10 cm spacing."},
            {"day": 20, "task": "💊 Gypsum Application",
                "detail": "Apply Gypsum 200kg/acre for better pod filling."},
            {"day": 45, "task": "🏗️ Pegging Stage",
                "detail": "Don't disturb soil. Maintain moisture for peg entry."},
            {"day": 75, "task": "🐛 Ticca Leaf Spot",
                "detail": "Spray Carbendazim if spots appear on leaves."},
            {"day": 105, "task": "🏁 Harvesting",
                "detail": "Harvest when inner shell turns dark/brown. Dry pods."}
        ]
    },
    "cotton": {
        "sowing_months": "Aug - Sept",
        "harvesting_months": "Jan - March",
        "duration_days": 160,
        "schedule": [
            {"day": 0, "task": "🌱 Sowing",
                "detail": "Sow 1.2kg Bt Cotton seeds per acre."},
            {"day": 30, "task": "💊 First Fertilizer",
                "detail": "Apply 20:20:20 NPK per acre."},
            {"day": 60, "task": "🌿 Squaring Stage",
                "detail": "Monitor for Pink Bollworm. Spray neem oil."},
            {"day": 90, "task": "🌸 Peak Flowering",
                "detail": "Apply Urea 25kg/acre. Avoid water stress."},
            {"day": 130, "task": "📦 Boll Opening",
                "detail": "Ensure dry weather for opening bolls. 1st picking."},
            {"day": 160, "task": "🏁 Final Picking",
                "detail": "Complete 3-4 pickings. Clean field for next crop."}
        ]
    },
    "maize": {
        "sowing_months": "June - July / Nov - Dec",
        "harvesting_months": "100-110 days",
        "duration_days": 105,
        "schedule": [
            {"day": 0, "task": "🌱 Sowing",
                "detail": "Sow 8-10kg hybrid seeds per acre."},
            {"day": 25, "task": "🌿 Knee High Stage",
                "detail": "Top dress Urea 35kg/acre. Weeding."},
            {"day": 50, "task": "🌽 Tasseling Stage",
                "detail": "Critical moisture period. Apply P&K fertilizer."},
            {"day": 75, "task": "📦 Milk Stage",
                "detail": "Monitor for Fall Armyworm. Spray recommended bio-pesticide."},
            {"day": 105, "task": "🏁 Harvesting",
                "detail": "Harvest when grains are hard and husks turn yellow."}
        ]
    },
    "turmeric": {
        "sowing_months": "May - June",
        "harvesting_months": "Jan - Feb",
        "duration_days": 270,
        "schedule": [
            {"day": 0, "task": "🌱 Rhizome Planting",
                "detail": "Plant mother/finger rhizomes in ridges."},
            {"day": 60, "task": "💊 First Manuring",
                "detail": "Apply Urea 25kg and MOP 15kg."},
            {"day": 120, "task": "🌿 Rhizome Growth",
                "detail": "Earthing up operation. Maintain moist conditions."},
            {"day": 180, "task": "💊 Second Dose",
                "detail": "Final fertilizer dose. Check for Rhizome rot."},
            {"day": 240, "task": "💧 Drying Phase",
                "detail": "Stop irrigation 15 days before harvesting."},
            {"day": 270, "task": "🏁 Harvest",
                "detail": "Dig rhizomes. Cure and dry for market."}
        ]
    },
    "onion": {
        "sowing_months": "Oct - Nov / May - June",
        "harvesting_months": "90-100 days",
        "duration_days": 95,
        "schedule": [
            {"day": 0, "task": "🌱 Bulb Planting",
                "detail": "Plant small bulbs or transplant seedlings."},
            {"day": 30, "task": "💊 Fertilizer",
                "detail": "Top dress Urea 20kg per acre."},
            {"day": 60, "task": "🌿 Bulb Formation",
                "detail": "Maintain regular light irrigation. Weed manually."},
            {"day": 80, "task": "📦 Maturing",
                "detail": "Neck fall indicates maturity. Stop watering."},
            {"day": 95, "task": "🏁 Harvesting",
                "detail": "Harvest and cure in shade for 3-4 days."}
        ]
    },
    "sorghum": {
        "sowing_months": "June - July / Jan - Feb",
        "harvesting_months": "100-115 days",
        "duration_days": 110,
        "schedule": [
            {"day": 0, "task": "🌱 Sowing",
                "detail": "Sow 4-6kg seeds per acre with 45x15 cm spacing."},
            {"day": 30, "task": "💊 Top Dressing",
                "detail": "Apply Urea 20kg per acre. Weeding and hoeing."},
            {"day": 60, "task": "🌾 Boot Stage",
                "detail": "Critical for moisture. Watch for Sorghum Midges."},
            {"day": 110, "task": "🏁 Harvesting",
                "detail": "Harvest when grain moisture is below 20%. Sun dry panicles."}
        ]
    },
    "black_gram": {
        "sowing_months": "Jan - Feb / June - July",
        "harvesting_months": "75-80 days",
        "duration_days": 80,
        "schedule": [
            {"day": 0, "task": "🌱 Sowing",
                "detail": "Sow 8-10kg seeds per acre. Treat with Rhizobium."},
            {"day": 20, "task": "🚿 Irrigation",
                "detail": "First irrigation if dry. One weeding."},
            {"day": 45, "task": "🌸 Flowering",
                "detail": "Foliar spray of 2% DAP for better pod set."},
            {"day": 80, "task": "🏁 Harvesting",
                "detail": "Harvest when 80% pods turn black."}
        ]
    },
    "green_gram": {
        "sowing_months": "Jan - Feb / Oct - Nov",
        "harvesting_months": "65-75 days",
        "duration_days": 75,
        "schedule": [
            {"day": 0, "task": "🌱 Sowing",
                "detail": "Sow 8kg seeds per acre. Treat with Phosphorus Solubilizing Bacteria."},
            {"day": 25, "task": "🌿 Pre-flowering",
                "detail": "Keep field weed-free. Monitor for Whitefly (YMV carrier)."},
            {"day": 50, "task": "📦 Pod Filling",
                "detail": "Spray 1% Urea for better grain quality."},
            {"day": 75, "task": "🏁 Harvesting",
                "detail": "Harvest in 2-3 pickings as pods ripen."}
        ]
    },
    "red_gram": {
        "sowing_months": "June - July",
        "harvesting_months": "150-180 days",
        "duration_days": 165,
        "schedule": [
            {"day": 0, "task": "🌱 Sowing",
                "detail": "Sow 5kg seeds per acre. Intercrop with groundnut/maize."},
            {"day": 45, "task": "🌿 Vegetative Phase",
                "detail": "Earthing up. Watch for Wilt disease."},
            {"day": 90, "task": "🌸 Flower Initiation",
                "detail": "Spray for Maruca vitrata (pod borer) if needed."},
            {"day": 165, "task": "🏁 Harvesting",
                "detail": "Harvest when pods turn dark and rattle."}
        ]
    },
    "chilli": {
        "sowing_months": "June - July / Jan - Feb",
        "harvesting_months": "150-180 days",
        "duration_days": 150,
        "schedule": [
            {"day": 0, "task": "🌱 Nursery Sowing",
                "detail": "Sow seeds in trays. Transplant in 35-40 days."},
            {"day": 40, "task": "🌿 Transplanting",
                "detail": "Transplant seedlings. Apply 5 tons FYM/acre."},
            {"day": 70, "task": "💊 First Fertilization",
                "detail": "Apply Urea 20kg + MOP 15kg."},
            {"day": 100, "task": "🌸 Peak Flowering",
                "detail": "Watch for Thrips/Mites. Use organic pesticides."},
            {"day": 120, "task": "🌶️ Green Chilli Picking",
                "detail": "Start picking for green chillies every 10 days."},
            {"day": 150, "task": "🏁 Dry Fruit Harvest",
                "detail": "Harvest fully ripe red fruits for drying."}
        ]
    },
    "ragi": {
        "sowing_months": "June - July / Dec - Jan",
        "harvesting_months": "100-110 days",
        "duration_days": 105,
        "schedule": [
            {"day": 0, "task": "🌱 Sowing/Transplanting",
                "detail": "Sow 5kg seeds in nursery or direct sow 4kg seeds/acre."},
            {"day": 20, "task": "💊 First Fertilizer",
                "detail": "Apply 15kg Nitrogen and 15kg Potash."},
            {"day": 40, "task": "🌿 Vegetative Phase",
                "detail": "Top dress 15kg Nitrogen. Intercultural operation/weeding."},
            {"day": 65, "task": "🌾 Flowering Stage",
                "detail": "Critical moisture requirement. Watch for Blast disease."},
            {"day": 105, "task": "🏁 Harvesting",
                "detail": "Harvest when earheads turn brown. Thresh and sun dry."}
        ]
    }
}


@calendar_bp.route('/crop-calendar', methods=['POST'])
def get_crop_calendar():
    data = request.get_json()
    crop = data.get('crop', 'rice').lower()
    sowing_date_str = data.get('sowing_date')

    crop_info = CROP_CALENDAR.get(crop)
    if not crop_info:
        return jsonify({"error": "Standard calendar for this crop is coming soon! Use the AI Chatbot for custom schedules."}), 404

    # Calculate actual dates
    sowing_date = datetime.strptime(
        sowing_date_str, "%Y-%m-%d") if sowing_date_str else datetime.now()
    duration = int(crop_info.get('duration_days', 100))
    harvest_date = sowing_date + timedelta(days=duration)

    # Add actual date to each schedule item
    scheduled_tasks = []
    today = datetime.now()
    schedule = crop_info.get('schedule', [])
    if isinstance(schedule, list):
        for item in schedule:
            if isinstance(item, dict):
                task_day = int(item.get('day', 0))
                task_date = sowing_date + timedelta(days=task_day)
                status = "completed" if task_date < today else "upcoming"
                if 0 <= (task_date - today).days <= 5:
                    status = "due-soon"

                scheduled_tasks.append({
                    "day": task_day,
                    "task": str(item.get('task', '')),
                    "detail": str(item.get('detail', '')),
                    "date": task_date.strftime("%d %b %Y"),
                    "status": status
                })

    return jsonify({
        "crop": crop.title(),
        "sowing_date": sowing_date.strftime("%d %b %Y"),
        "harvest_date": harvest_date.strftime("%d %b %Y"),
        "duration_days": duration,
        "sowing_months": str(crop_info.get('sowing_months', '')),
        "tasks": scheduled_tasks
    }), 200


@calendar_bp.route('/crop-calendar/crops', methods=['GET'])
def list_crops():
    return jsonify(list(CROP_CALENDAR.keys())), 200
