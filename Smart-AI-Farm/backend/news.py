from flask import Blueprint, jsonify

news_bp = Blueprint('news', __name__)


@news_bp.route('/news', methods=['GET'])
def get_news():
    # In a real-world scenario, you would fetch from Google News API or a localized agriculture feed.
    # Using curated static recent and relevant data for the demonstration and 24/7 reliability.

    from datetime import datetime, timedelta

    # Use a stable start-of-day for 'today' to avoid the notification badge always showing
    # a new item due to millisecond differences in dynamic timestamps.
    today_now = datetime.now()
    today = today_now.replace(hour=0, minute=0, second=0, microsecond=0)

    dates = {
        "today": today,
        "yesterday": today - timedelta(days=1),
        "last_week": today - timedelta(days=7),
        "one_month": today - timedelta(days=30),
        "three_months": today - timedelta(days=90),
        "six_months": today - timedelta(days=180)
    }

    mock_news = [
        {
            "id": 1,
            "title": "TN Govt: ₹2000 Farmer Incentive for Harvest Season Announced",
            "source": "Tamil Nadu Agriculture Dept",
            "date": dates["today"].strftime("%Y-%m-%d"),
            "timestamp": dates["today"].timestamp(),
            "summary": "Special Pongal harvest incentive of ₹2000 per acre for paddy farmers in Delta districts.",
            "full_text": "The Honorable Chief Minister of Tamil Nadu has approved a special harvest incentive package. Farmers in Tanjore, Trichy, and Nagapattinam districts who have registered for the 2026 Kuruvai season will receive ₹2000 directly into their accounts."
        },
        {
            "id": 2,
            "title": "Central Govt: New Solar Pump Subsidy (PM-KUSUM) 2026 Update",
            "source": "Ministry of New & Renewable Energy",
            "date": dates["yesterday"].strftime("%Y-%m-%d"),
            "timestamp": dates["yesterday"].timestamp(),
            "summary": "Farmers can now get 90% subsidy for 5HP to 10HP Solar Water Pumps.",
            "full_text": "Under the PM-KUSUM Component-B, the central government has increased the subsidy cap for small farmers."
        },
        {
            "id": 3,
            "title": "MSP Update: Paddy Long Grain price increased",
            "source": "Agrigov.in News",
            "date": dates["last_week"].strftime("%Y-%m-%d"),
            "timestamp": dates["last_week"].timestamp(),
            "summary": "Minimum Support Price for Long Grain Paddy increased by ₹143 per Quintal.",
            "full_text": "The new price for Paddy (Grade A) will be ₹2,323 per quintal for the next season."
        },
        {
            "id": 4,
            "title": "New Organic Fertilizer Subsidy Policy",
            "source": "Fertilizer Dept",
            "date": dates["one_month"].strftime("%Y-%m-%d"),
            "timestamp": dates["one_month"].timestamp(),
            "summary": "Govt promotes organic farming with 40% subsidy on bio-fertilizers.",
            "full_text": "A new circular has been issued to promote sustainable agriculture by providing direct subsidies to organic manure producers and farmers using bio-fertilizers."
        },
        {
            "id": 5,
            "title": "Monsoon Prediction 2026: Normal Rainfall Expected",
            "source": "IMD Weather",
            "date": dates["three_months"].strftime("%Y-%m-%d"),
            "timestamp": dates["three_months"].timestamp(),
            "summary": "IMD predicts a healthy monsoon season across South India.",
            "full_text": "Initial models suggest a 98% probability of normal rainfall, which is great news for rainfed agriculture in Tamil Nadu."
        },
        {
            "id": 6,
            "title": "Smart Irrigation Workshop for Small Farmers",
            "source": "Agri Tech Corp",
            "date": dates["six_months"].strftime("%Y-%m-%d"),
            "timestamp": dates["six_months"].timestamp(),
            "summary": "Free training on drip irrigation and water management.",
            "full_text": "This workshop covered the benefits of sensor-based irrigation and how it can save up to 40% of water compared to traditional methods."
        }
    ]

    # Sort by timestamp descending (newest first)
    mock_news.sort(key=lambda x: x['timestamp'], reverse=True)

    return jsonify(mock_news), 200
