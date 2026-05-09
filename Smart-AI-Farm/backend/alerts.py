import math
import urllib.request
import urllib.parse
import json
import ssl
import xml.etree.ElementTree as ET
from flask import Blueprint, jsonify, session, request
from datetime import datetime
from typing import Any, Dict, List
from backend.news import get_news

alerts_bp = Blueprint('alerts', __name__)


def calculate_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Haversine formula to calculate distance between two points in km."""
    R = 6371
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat/2)**2 + math.cos(math.radians(lat1)) * \
        math.cos(math.radians(lat2)) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))
    return R * c


def fetch_live_disasters(user_lat=None, user_lon=None):
    """Fetches real-time disaster alerts and filters by proximity if location is provided."""
    disasters = []
    try:
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE

        url = "https://www.gdacs.org/xml/rss.xml"
        req = urllib.request.Request(
            url, headers={'User-Agent': 'SmartFarmApp/1.0'})
        with urllib.request.urlopen(req, timeout=15, context=ctx) as response:
            xml_data = response.read()
            tree = ET.fromstring(xml_data)

            all_events = []
            # Define namespaces for GDACS
            namespaces = {
                'georss': 'http://www.georss.org/georss',
                'gdacs': 'http://www.gdacs.org/gdacs'
            }

            for item in tree.findall('.//item'):
                title_node = item.find('title')
                desc_node = item.find('description')
                if title_node is None:
                    continue

                title = str(
                    title_node.text) if title_node.text else "Unknown Event"
                description = str(desc_node.text) if (
                    desc_node is not None and desc_node.text) else ""

                # Severity
                risk = "Low"
                if "Orange" in title or "Orange" in description:
                    risk = "Medium"
                if "Red" in title or "Red" in description:
                    risk = "High"

                # Extract coordinates
                event_lat, event_lon = None, None
                point = item.find('georss:point', namespaces)
                if point is not None and point.text:
                    try:
                        p_txt = str(point.text).split()
                        if len(p_txt) == 2:
                            event_lat, event_lon = float(
                                p_txt[0]), float(p_txt[1])
                    except:
                        pass

                pub_date_node = item.find('pubDate')
                ts = datetime.now().timestamp()
                if pub_date_node is not None and pub_date_node.text:
                    try:
                        ts_text = str(pub_date_node.text).strip()
                        dt = datetime.strptime(
                            ts_text, '%a, %d %b %Y %H:%M:%S %Z')
                        ts = dt.timestamp()
                    except:
                        pass

                event = {
                    "type": title.split(' in ')[0] if ' in ' in title else "Alert",
                    "risk_level": risk,
                    "message": title,
                    "action": "Check local weather reports and secure harvest.",
                    "timestamp": ts,
                    "lat": event_lat,
                    "lon": event_lon
                }

                if user_lat is not None and user_lon is not None and event_lat is not None and event_lon is not None:
                    try:
                        dist = calculate_distance(
                            float(user_lat), float(user_lon), event_lat, event_lon)
                        event['distance'] = round(dist)

                        # FILTER LOGIC:
                        # 1. Always show High Risk events within 5000km
                        # 2. Show Medium Risk within 2000km
                        # 3. Show Low Risk only if very close (within 500km)
                        if (risk == "High" and dist < 5000) or \
                           (risk == "Medium" and dist < 2000) or \
                           (risk == "Low" and dist < 500):
                            all_events.append(event)
                    except:
                        all_events.append(event)
                else:
                    # No location known, show major global events
                    if risk in ["High", "Medium"]:
                        all_events.append(event)

            # Sort by distance if location known, else by time
            if user_lat is not None and user_lon is not None:
                all_events.sort(key=lambda x: x.get('distance', 999999))
            else:
                all_events.sort(key=lambda x: x['timestamp'], reverse=True)

            # Limit to top 5
            # Limit to top 5 safely
            disasters: List[Dict[str, Any]] = []
            count = 0
            for ev in all_events:
                if count >= 5:
                    break
                disasters.append(ev)
                count += 1
    except Exception as e:
        print("GDACS API Error:", e)
    return disasters


def fetch_weather_alerts(lat, lon):
    """Fetches weather-based specific alerts (cyclone, rain, etc.) from Open-Meteo."""
    alerts = []
    if not lat or not lon:
        return alerts

    try:
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE

        # We check both current and daily forecast for precipitation probability and temperature
        url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=precipitation,wind_speed_10m,temperature_2m&daily=precipitation_probability_max,temperature_2m_max&timezone=auto"
        req = urllib.request.Request(
            url, headers={'User-Agent': 'SmartFarmApp/1.0'})
        with urllib.request.urlopen(req, timeout=15, context=ctx) as response:
            data = json.loads(response.read().decode())
            curr = data.get('current', {})
            daily = data.get('daily', {})

            wind_speed = curr.get('wind_speed_10m', 0)
            precip = curr.get('precipitation', 0)
            rain_prob = daily.get('precipitation_probability_max', [0])[0]
            temp = curr.get('temperature_2m') or daily.get(
                'temperature_2m_max', [0])[0]

            # 1. Cyclone / High Winds
            if wind_speed > 60:
                alerts.append({
                    "type": "Cyclone Alert",
                    "risk_level": "High",
                    "message": f"Extreme winds ({wind_speed} km/h) detected! Potential cyclone conditions.",
                    "action": "Secure all farm equipment and stay indoors.",
                    "timestamp": datetime.now().timestamp()
                })
            elif wind_speed > 40:
                alerts.append({
                    "type": "Wind Warning",
                    "risk_level": "Medium",
                    "message": f"Strong winds ({wind_speed} km/h). Avoid spraying and protect tall crops.",
                    "action": "Check structural supports for greenhouses.",
                    "timestamp": datetime.now().timestamp()
                })

            # 2. Rain Possibility
            if precip > 5:
                alerts.append({
                    "type": "Rain Alert",
                    "risk_level": "High",
                    "message": "Heavy rainfall currently detected in your area.",
                    "action": "Ensure drainage channels are clear to prevent flooding.",
                    "timestamp": datetime.now().timestamp()
                })
            elif rain_prob > 70:
                alerts.append({
                    "type": "Rain Possibility",
                    "risk_level": "Medium",
                    "message": f"High probability of rain ({rain_prob}%) in the next 24 hours.",
                    "action": "Adjust irrigation schedules and consider postponing harvest.",
                    "timestamp": datetime.now().timestamp()
                })
            elif rain_prob > 40:
                alerts.append({
                    "type": "Light Rain",
                    "risk_level": "Low",
                    "message": f"Scattered showers possible ({rain_prob}%).",
                    "action": "Monitor weather updates.",
                    "timestamp": datetime.now().timestamp()
                })

            # 3. Heatwave / Temperature
            if temp > 40:
                alerts.append({
                    "type": "Heatwave Warning",
                    "risk_level": "High",
                    "message": f"Extreme heat ({temp}°C) detected. High risk of crop wilting.",
                    "action": "Increase irrigation frequency and provide shade if possible.",
                    "timestamp": datetime.now().timestamp()
                })
            elif temp > 35:
                alerts.append({
                    "type": "High Temperature",
                    "risk_level": "Medium",
                    "message": f"High temperature ({temp}°C) recorded. Monitor soil moisture.",
                    "action": "Water crops during early morning or late evening.",
                    "timestamp": datetime.now().timestamp()
                })

    except Exception as e:
        print("Weather Alerts Fetch Error:", e)

    return alerts


def fetch_weekly_disaster_forecast(lat, lon):
    """Analyzes the 7-day forecast for potential disasters and risks."""
    forecast_alerts = []
    if not lat or not lon:
        return forecast_alerts

    try:
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE

        # Request 7-day daily forecast for rain, wind, and temperature
        url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&daily=precipitation_sum,precipitation_probability_max,wind_speed_10m_max,temperature_2m_max&timezone=auto"
        req = urllib.request.Request(
            url, headers={'User-Agent': 'SmartFarmApp/1.0'})
        with urllib.request.urlopen(req, timeout=15, context=ctx) as response:
            data = json.loads(response.read().decode())
            daily = data.get('daily', {})
            times = daily.get('time', [])
            rain_sums = daily.get('precipitation_sum', [])
            rain_probs = daily.get('precipitation_probability_max', [])
            wind_maxs = daily.get('wind_speed_10m_max', [])
            temp_maxs = daily.get('temperature_2m_max', [])

            for i in range(1, len(times)):  # Start from tomorrow (index 1)
                date_str = times[i]
                dt = datetime.strptime(date_str, "%Y-%m-%d")
                day_name = dt.strftime("%A, %d %b")
                ts = dt.timestamp()

                # 1. Extreme Rain / Flood Risk
                if rain_sums[i] > 30:
                    forecast_alerts.append({
                        "type": "Heavy Rain Forecast",
                        "risk_level": "High",
                        "message": f"Extreme rain ({rain_sums[i]}mm) forecast for {day_name}. High flood risk.",
                        "action": "Clear drainage and secure low-lying areas.",
                        "timestamp": ts,
                        "date": day_name
                    })
                elif rain_probs[i] > 80:
                    forecast_alerts.append({
                        "type": "Rain Expected",
                        "risk_level": "Medium",
                        "message": f"Strong possibility of rain ({rain_probs[i]}%) on {day_name}.",
                        "action": "Plan harvesting or spraying before this date.",
                        "timestamp": ts,
                        "date": day_name
                    })

                # 2. Cyclone / High Wind Risk
                if wind_maxs[i] > 50:
                    forecast_alerts.append({
                        "type": "High Wind Forecast",
                        "risk_level": "High",
                        "message": f"Dangerous winds ({wind_maxs[i]}km/h) expected on {day_name}.",
                        "action": "Secure greenhouses and nursery structures.",
                        "timestamp": ts,
                        "date": day_name
                    })

                # 3. Heatwave Risk
                if temp_maxs[i] > 42:
                    forecast_alerts.append({
                        "type": "Heatwave Forecast",
                        "risk_level": "High",
                        "message": f"Severe heatwave ({temp_maxs[i]}°C) predicted for {day_name}.",
                        "action": "Ensure intense irrigation and livestock protection.",
                        "timestamp": ts,
                        "date": day_name
                    })

    except Exception as e:
        print("Weekly Forecast Fetch Error:", e)

    return forecast_alerts


@alerts_bp.route('/alerts', methods=['GET'])
def get_alerts():
    user_lat = request.args.get('lat')
    user_lon = request.args.get('lon')
    city_name = request.args.get('city')

    # If city is provided, resolve it to coordinates for filtering
    if city_name and not user_lat:
        try:
            ctx = ssl.create_default_context()
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE

            geo_url = f"https://nominatim.openstreetmap.org/search?q={urllib.parse.quote(city_name)}&format=json&limit=1"
            req = urllib.request.Request(
                geo_url, headers={'User-Agent': 'SmartFarmApp/2.0'})
            with urllib.request.urlopen(req, timeout=15, context=ctx) as response:
                geo_data = json.loads(response.read().decode())
                if geo_data:
                    user_lat, user_lon = geo_data[0]['lat'], geo_data[0]['lon']
        except:
            pass

    live_disasters = fetch_live_disasters(user_lat, user_lon)
    weather_alerts = fetch_weather_alerts(user_lat, user_lon)
    weekly_forecast = fetch_weekly_disaster_forecast(user_lat, user_lon)

    # Merge and sort
    all_alerts = weather_alerts + live_disasters
    all_alerts.sort(key=lambda x: x['timestamp'], reverse=True)

    return jsonify({
        "disaster": all_alerts,
        "forecast": weekly_forecast,
        "crop": [
            {
                "type": "Pest Outbreak",
                "risk_level": "Medium",
                "message": "Aphids detected in nearby districts. Monitor crop leaves carefully.",
                "action": "Apply organic neem spray as a preventative measure.",
                "timestamp": datetime.now().replace(hour=0, minute=0, second=0, microsecond=0).timestamp()
            }
        ]
    }), 200


@alerts_bp.route('/notifications/count', methods=['GET'])
def get_notification_count():
    last_viewed = session.get('last_notification_check', 0)

    user_lat = request.args.get('lat')
    user_lon = request.args.get('lon')
    city_name = request.args.get('city')

    # Resolve city for count if needed
    if city_name and not user_lat:
        try:
            ctx = ssl.create_default_context()
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE
            geo_url = f"https://nominatim.openstreetmap.org/search?q={urllib.parse.quote(city_name)}&format=json&limit=1"
            req = urllib.request.Request(
                geo_url, headers={'User-Agent': 'SmartFarmApp/2.0'})
            with urllib.request.urlopen(req, timeout=15, context=ctx) as response:
                geo_data = json.loads(response.read().decode())
                if geo_data:
                    user_lat, user_lon = geo_data[0]['lat'], geo_data[0]['lon']
        except:
            pass

    # 1. News
    news_data, _ = get_news()
    news_list = news_data.get_json() or []
    unread_news = [n for n in news_list if n.get('timestamp', 0) > last_viewed]

    # 2. Alerts (Disasters)
    disasters = fetch_live_disasters(user_lat, user_lon)
    unread_alerts = [d for d in disasters if d.get(
        'timestamp', 0) > last_viewed]

    # 3. Schemes (Mock: if never checked, show 2)
    unread_schemes_count = 0
    if last_viewed == 0:
        unread_schemes_count = 2

    total_unread = len(unread_news) + len(unread_alerts) + unread_schemes_count

    return jsonify({
        "count": total_unread,
        "last_checked": last_viewed
    }), 200


@alerts_bp.route('/notifications/mark-read', methods=['POST'])
def mark_notifications_read():
    session['last_notification_check'] = datetime.now().timestamp()
    session.modified = True
    return jsonify({"status": "success"}), 200
