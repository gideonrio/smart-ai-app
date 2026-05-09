from flask import Blueprint, request, jsonify

reminder_bp = Blueprint('reminder', __name__)

# Temporary mock store
REMINDERS = []


@reminder_bp.route('/reminder', methods=['POST'])
def add_reminder():
    data = request.json
    try:
        reminder = {
            "id": len(REMINDERS) + 1,
            "crop": data['crop'],
            "date": data['date'],
            "time": data['time'],
            "type": data['type'],  # Pesticide, Irrigation, Fertilizer, Harvest
            "message": data['message'],
            "alarm": data.get('alarm', False),
            "ringtone": data.get('ringtone', 'classic')
        }
        REMINDERS.append(reminder)
        return jsonify({"message": "Reminder set successfully", "reminder": reminder}), 201
    except KeyError as e:
        return jsonify({"error": f"Missing field {e}"}), 400


@reminder_bp.route('/reminders', methods=['GET'])
def get_reminders():
    return jsonify(REMINDERS), 200
