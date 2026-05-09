from flask import Blueprint, jsonify, request

schemes_bp = Blueprint('schemes', __name__)

ALL_SCHEMES = [
    {
        "id": 0, "title": "TN Farmer Identity Card (Dept. of Agriculture)", "category": "Essential Document",
        "amount": "Universal Benefit Access", "crop": "All", "land_limit": 100,
        "description": "The primary identity document for all farmers in Tamil Nadu. Required to access Uzhavar Santhai, subsidies, and govt procurement centers.",
        "eligibility": "All land-holding farmers in Tamil Nadu. Essential for identifying genuine cultivators.",
        "documents": "Aadhaar Card, Patta/Chitta copy, Passport Size Photo",
        "link": "https://www.tnagrisnet.tn.gov.in/"
    },
    {
        "id": 1, "title": "PM Kisan Samman Nidhi (Govt of India)", "category": "Financial Assistance",
        "amount": "₹6,000/year", "crop": "All", "land_limit": 2,
        "description": "Central Govt scheme providing ₹6,000 per year as minimum income support to farmers. Paid in 3 installments of ₹2,000.",
        "eligibility": "Small and marginal farmers across India with cultivable land up to 2 hectares.",
        "documents": "Aadhaar Card, Patta/Chitta, Bank Passbook",
        "link": "https://pmkisan.gov.in/"
    },
    {
        "id": 2, "title": "Uzhavar Santhai Scheme (Govt of Tamil Nadu)", "category": "Market",
        "amount": "Direct Market Access", "crop": "Vegetables & Fruits", "land_limit": 100,
        "description": "Tamil Nadu Govt initiative allowing farmers to sell their produce directly to consumers without middlemen. Requires a valid Farmer ID card.",
        "eligibility": "All farmers in Tamil Nadu holding an identity card issued by the Department of Agriculture.",
        "documents": "Farmer ID Card, Aadhaar, Passport Photo",
        "link": "https://www.tnagrisnet.tn.gov.in/"
    },
    {
        "id": 3, "title": "Kuruvai Special Package (Govt of Tamil Nadu)", "category": "Financial Assistance",
        "amount": "Input Subsidy", "crop": "Paddy", "land_limit": 100,
        "description": "Special assistance package for Delta farmers in Tamil Nadu for Kuruvai paddy cultivation, providing seeds, fertilizers, and equipment subsidies.",
        "eligibility": "Paddy farmers in the Delta districts of Tamil Nadu.",
        "documents": "Adangal, Chitta, Bank Account",
        "link": "https://www.tnagrisnet.tn.gov.in/"
    },
    {
        "id": 4, "title": "Kisan Credit Card (KCC) Loan (Govt of India)", "category": "Loan",
        "amount": "Up to ₹3 Lakh at 4% interest", "crop": "All", "land_limit": 100,
        "description": "Central crop loan scheme at 7% interest rate. Timely repayment provides 3% subvention, making the effective rate 4%. Supported by Indian banks.",
        "eligibility": "All Indian farmers, sharecroppers, tenant farmers.",
        "documents": "Aadhaar, Patta, Passport Photo",
        "link": "https://sbi.co.in/web/agri-rural/agriculture-banking/crop-loan/kisan-credit-card"
    },
    {
        "id": 5, "title": "Pradhan Mantri Fasal Bima Yojana (Govt of India)", "category": "Crop Insurance",
        "amount": "Comprehensive Cover", "crop": "Notified Crops", "land_limit": 100,
        "description": "National crop insurance scheme covering damages from natural calamities, pests, and diseases. Premium is 1.5% to 2%.",
        "eligibility": "Farmers growing notified crops in notified areas across India.",
        "documents": "Land Records, Aadhaar, Bank Account",
        "link": "https://pmfby.gov.in/"
    },
    {
        "id": 6, "title": "TN Micro Irrigation Scheme (Govt of Tamil Nadu)", "category": "Irrigation",
        "amount": "100% subsidy for small farmers", "crop": "All", "land_limit": 100,
        "description": "Tamil Nadu Govt provides 100% subsidy for small/marginal farmers and 75% for other farmers to install drip and sprinkler irrigation systems.",
        "eligibility": "All farmers in Tamil Nadu. Preference given to water-depleted blocks.",
        "documents": "Patta, Chitta, FM Sketch, Aadhaar",
        "link": "https://tnhorticulture.tn.gov.in/horti/mimis/"
    },
    {
        "id": 7, "title": "Agri Infrastructure Fund (Govt of India)", "category": "Loan",
        "amount": "Up to ₹2 Crore at 3% subvention", "crop": "All", "land_limit": 100,
        "description": "Financing facility for post-harvest management infrastructure and community farming assets. 3% interest subvention and credit guarantee.",
        "eligibility": "Farmers, FPOs, PACS, Startups across India.",
        "documents": "DPR, KYC Documents, Bank Account",
        "link": "https://agriinfra.dac.gov.in/"
    },
    {
        "id": 8, "title": "Kalaignarin All Village Integrated Agri Development Programme (Govt of Tamil Nadu)", "category": "Development",
        "amount": "Village-level infra", "crop": "All", "land_limit": 100,
        "description": "TN Government initiative focusing on bringing fallow lands into cultivation, creating water resources, and overall village agricultural development.",
        "eligibility": "Villages identified under the scheme in Tamil Nadu.",
        "documents": "Determined at Panchayat level",
        "link": "https://www.tnagrisnet.tn.gov.in/"
    }
]


@schemes_bp.route('/schemes_data', methods=['GET'])
def get_schemes():
    request.args.get('state', None)
    category = request.args.get('category', None)
    land_size = request.args.get('land_size', None)

    filtered = ALL_SCHEMES.copy()

    if category and category != 'All':
        filtered = [s for s in filtered if s['category'] == category]

    if land_size:
        try:
            ls = float(land_size)
            filtered = [s for s in filtered if s['land_limit'] >= ls]
        except:
            pass

    return jsonify(filtered), 200
