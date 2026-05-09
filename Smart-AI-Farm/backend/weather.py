import urllib.request
import urllib.parse
import json
import ssl
from flask import Blueprint, request, jsonify
from datetime import datetime

weather_bp = Blueprint('weather', __name__)


def get_city_name(lat, lon):
    try:
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE

        url = f"https://nominatim.openstreetmap.org/reverse?lat={lat}&lon={lon}&format=json&addressdetails=1"
        req = urllib.request.Request(
            url, headers={'User-Agent': 'SmartFarmApp/3.0'})
        with urllib.request.urlopen(req, timeout=15, context=ctx) as response:
            data = json.loads(response.read().decode())
            if 'address' in data:
                addr = data['address']

                # Priority: neighbourhood -> suburb -> quarter -> village -> town
                locality = addr.get('neighbourhood') or addr.get('suburb') or addr.get(
                    'quarter') or addr.get('village') or addr.get('town')
                city = addr.get('city') or addr.get(
                    'town') or addr.get('municipality') or "Chennai"

                if locality and city:
                    # Clean up if locality is same as city
                    if locality.lower() == city.lower():
                        return city.capitalize()
                    return f"{locality}, {city}"
                return city or "Chennai"
    except Exception as e:
        print("Geocode Error:", e)
    return "Chennai"


def get_weather_condition(weather_code):
    # WMO Weather interpretation codes
    if weather_code == 0:
        return "Clear sky"
    if weather_code in [1, 2, 3]:
        return "Partly cloudy"
    if weather_code in [45, 48]:
        return "Foggy"
    if weather_code in [51, 53, 55, 56, 57]:
        return "Drizzle"
    if weather_code in [61, 63, 65, 66, 67]:
        return "Rainy"
    if weather_code in [71, 73, 75, 77]:
        return "Snow"
    if weather_code in [80, 81, 82]:
        return "Rain showers"
    if weather_code in [85, 86]:
        return "Snow showers"
    if weather_code in [95, 96, 99]:
        return "Thunderstorm"
    return "Unknown"


@weather_bp.route('/weather', methods=['GET'])
def get_weather():
    lat = request.args.get('lat')
    lon = request.args.get('lon')
    city_name_query = request.args.get('city')

    location_name = "Locating..."

    # If city name is provided manually
    if city_name_query:
        try:
            ctx = ssl.create_default_context()
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE

            # Resolve city name to coordinates with full address details
            geo_url = f"https://nominatim.openstreetmap.org/search?q={urllib.parse.quote(city_name_query)}&format=json&limit=1&addressdetails=1"
            req = urllib.request.Request(
                geo_url, headers={'User-Agent': 'SmartFarmApp/2.0'})
            with urllib.request.urlopen(req, timeout=15, context=ctx) as response:
                geo_data = json.loads(response.read().decode())
                if geo_data:
                    res = geo_data[0]
                    lat, lon = res['lat'], res['lon']
                    # Smart locality extraction
                    addr = res.get('address', {})
                    locality = addr.get('neighbourhood') or addr.get('suburb') or addr.get(
                        'quarter') or addr.get('village') or addr.get('town')
                    city = addr.get('city') or addr.get(
                        'town') or city_name_query.capitalize()

                    if locality and city:
                        if locality.lower() == city.lower():
                            location_name = city
                        else:
                            location_name = f"{locality}, {city}"
                    else:
                        location_name = city
                else:
                    return jsonify({"error": "City not found"}), 404
        except Exception as e:
            print("Geo Search Error:", e)
            lat, lon = "13.0827", "80.2707"
            location_name = city_name_query.capitalize()

    if not lat or not lon:
        lat, lon = "13.0827", "80.2707"  # Default to Chennai
        location_name = "Chennai, Tamil Nadu"
    elif not city_name_query:
        location_name = get_city_name(lat, lon)

    try:
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE

        open_meteo_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,relative_humidity_2m,precipitation,weather_code,wind_speed_10m&daily=weather_code,temperature_2m_max,temperature_2m_min,precipitation_probability_max&timezone=auto"
        req = urllib.request.Request(open_meteo_url)
        with urllib.request.urlopen(req, timeout=15, context=ctx) as response:
            data = json.loads(response.read().decode())

            curr = data['current']
            daily = data['daily']

            temp = curr['temperature_2m']
            humidity = curr['relative_humidity_2m']
            wind = curr['wind_speed_10m']
            cond_code = curr['weather_code']
            condition = get_weather_condition(cond_code)

            alerts = []
            if wind > 60:
                alerts.append(
                    "🌀 Cyclone/High Wind Alert! Secure crops and equipment.")
            elif wind > 40:
                alerts.append(
                    "🌬️ Strong Winds Warning. Avoid pesticide spraying.")

            if curr['precipitation'] > 10 or (daily['precipitation_probability_max'] and daily['precipitation_probability_max'][0] > 80):
                alerts.append(
                    "🌧️ Heavy Rain Expected! Ensure proper drainage in fields.")

            if curr['temperature_2m'] > 40:
                alerts.append(
                    "🔥 Heatwave Warning! Keep crops and livestock hydrated.")

            forecast = []
            d_times = daily.get('time', [])
            d_temps_max = daily.get('temperature_2m_max', [])
            d_temps_min = daily.get('temperature_2m_min', [])
            d_precip_prob = daily.get('precipitation_probability_max', [])

            for i in range(1, 6):  # next 5 days
                if i < len(d_times):
                    try:
                        day_date = datetime.strptime(
                            str(d_times[i]), "%Y-%m-%d").strftime("%A")
                        prob = d_precip_prob[i] if (
                            d_precip_prob and i < len(d_precip_prob)) else 0
                        t_max = d_temps_max[i] if (
                            d_temps_max and i < len(d_temps_max)) else 0
                        t_min = d_temps_min[i] if (
                            d_temps_min and i < len(d_temps_min)) else 0
                        forecast.append({
                            "day": day_date,
                            "rain_prob": prob,
                            "temp_max": t_max,
                            "temp_min": t_min
                        })
                    except:
                        pass

            return jsonify({
                "location": location_name,
                "current": {
                    "temp": round(temp),
                    "humidity": humidity,
                    "wind": wind,
                    "condition": condition
                },
                "alerts": alerts,
                "forecast": forecast
            }), 200

    except Exception as e:
        print("Weather API error:", e)
        return jsonify({
            "location": location_name,
            "current": {"temp": 32, "humidity": 75, "wind": 15, "condition": "Sunny (Fallback)"},
            "alerts": ["⚠️ Unable to fetch live weather data. Showing offline predictions."],
            "forecast": [
                {"day": "Tomorrow", "rain_prob": 10,
                    "temp_max": 33, "temp_min": 24},
                {"day": "Day 2", "rain_prob": 30, "temp_max": 31, "temp_min": 23}
            ]
        }), 200
