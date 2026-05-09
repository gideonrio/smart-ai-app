from flask import Blueprint, request, jsonify, session

auth_bp = Blueprint('auth', __name__)

# Temporary mock user DB for email
USERS = {
    "test@example.com": {
        "password": "password123",
        "name": "Farmer Raman",
        "location": "Tamil Nadu",
        "crop": "Paddy"
    }
}


@auth_bp.route('/get-profile', methods=['GET'])
def get_profile():
    email = session.get('user_email')
    if not email:
        return jsonify({"error": "Unauthorized"}), 401

    user = USERS.get(email, {})
    return jsonify(user), 200


@auth_bp.route('/update-profile', methods=['POST'])
def update_profile():
    email = session.get('user_email')
    if not email:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.json
    if email not in USERS:
        USERS[email] = {}

    USERS[email].update({
        "name": data.get("name"),
        "age": data.get("age"),
        "gender": data.get("gender"),
        "location": data.get("location"),
        "crop": data.get("crop"),
        "phone": data.get("phone")
    })

    return jsonify({"message": "Profile updated successfully!", "user": USERS[email]}), 200


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"error": "Email and password required"}), 400

    user = USERS.get(email)
    if not user or user.get("password") != password:
        # If user doesn't exist, we can register them for mock purposes
        if not user:
            USERS[email] = {
                "password": password,
                "name": email.split('@')[0],
                "location": "Unknown",
                "crop": "Unknown"
            }
            user = USERS[email]
        else:
            return jsonify({"error": "Invalid email or password"}), 401

    session['user_email'] = email

    return jsonify({
        "message": "Login successful",
        "user": {"name": user["name"], "email": email}
    }), 200
