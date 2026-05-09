from flask import Blueprint, request, jsonify, session
from datetime import datetime

wallet_bp = Blueprint('wallet', __name__)

# Simulated Government NPCI/DBT Database for demonstration
# In a real app, this would hit Govt API endpoints
GOVT_DBT_SERVER = [
    {"id": "DBT1001", "scheme": "PM-Kisan Samman Nidhi", "amount": 2000,
        "date": "2024-03-01", "status": "Credited", "ref": "NPCI-77BB82"},
    {"id": "DBT1002", "scheme": "Kuruvai Special Crop Package", "amount": 1500,
        "date": "2024-02-15", "status": "Credited", "ref": "NPCI-11AA93"},
    {"id": "DBT1003", "scheme": "Fertilizer Subsidy", "amount": 850,
        "date": "2024-02-01", "status": "Credited", "ref": "NPCI-44CC11"},
    {"id": "DBT1004", "scheme": "Fasal Bima Yojana (Insurance)", "amount": 5400,
     "date": "2024-01-20", "status": "Credited", "ref": "NPCI-99DD55"}
]


@wallet_bp.route('/wallet_history', methods=['GET'])
def get_wallet_history():
    # Check if account is linked in session
    is_linked = session.get('bank_linked', False)
    aadhaar_last4 = session.get('aadhaar_last4', "****")

    if not is_linked:
        return jsonify({
            "balance": 0,
            "transactions": [],
            "is_linked": False,
            "account_info": "Not Linked"
        })

    # Calculate total from Govt Data
    total_balance = sum(item['amount'] for item in GOVT_DBT_SERVER)

    return jsonify({
        "balance": total_balance,
        "transactions": GOVT_DBT_SERVER,
        "is_linked": True,
        "aadhaar": f"XXXX-XXXX-{aadhaar_last4}",
        "bank_name": session.get('bank_name', "State Bank of India")
    })


@wallet_bp.route('/verify_aadhaar', methods=['POST'])
def verify_aadhaar():
    """Simulates Aadhaar-linked Bank Account Verification (DBT Bharat Portal)"""
    data = request.json
    aadhaar = data.get('aadhaar')
    data.get('phone')

    if len(aadhaar) != 12:
        return jsonify({"success": False, "message": "Invalid Aadhaar Number (Must be 12 digits)"}), 400

    # Simulate a 1-second delay for Govt Server Lookup
    # In reality, this would call the UIDAI / NPCI API

    session['bank_linked'] = True
    session['aadhaar_last4'] = aadhaar[-4:]
    session['bank_name'] = "State Bank of India (Aadhaar Seeded)"
    session.modified = True

    return jsonify({
        "success": True,
        "message": "Bank Account Linked via Aadhaar DBT Bridge!",
        "bank": "State Bank of India",
        "kyc": "Verified"
    })


@wallet_bp.route('/refresh_subsidy', methods=['POST'])
def refresh_subsidy():
    """Simulates fetching the latest DBT credits from Govt Portal"""
    if not session.get('bank_linked'):
        return jsonify({"success": False, "message": "Please link your bank account first."}), 401

    return jsonify({
        "success": True,
        "message": "Synched with DBT Bharat Portal. 4 Transactions found.",
        "last_sync": datetime.now().strftime("%Y-%m-%d %H:%M")
    })
