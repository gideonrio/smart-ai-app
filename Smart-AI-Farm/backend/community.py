from flask import Blueprint, jsonify

community_bp = Blueprint('community', __name__)

POSTS = [
    {
        "id": 1,
        "author": "Ramesh Kumar",
        "avatar": "https://api.dicebear.com/7.x/avataaars/svg?seed=Ramesh",
        "time": "2 hours ago",
        "title": "Tomato Blatt Blight Issue",
        "content": "My tomato leaves are turning brown from the edges. Attached is the AI scan. What should I do?",
        "tags": ["Tomato", "Disease", "Help"],
        "likes": 12,
        "comments": 4
    },
    {
        "id": 2,
        "author": "Suresh Farm Expert",
        "avatar": "https://api.dicebear.com/7.x/avataaars/svg?seed=Suresh",
        "time": "5 hours ago",
        "title": "Best organic fertilizer for Cotton?",
        "content": "Looking for recommendations for high-yield organic fertilizers this season. I've tried Vermicompost so far.",
        "tags": ["Cotton", "Organic", "Fertilizer"],
        "likes": 34,
        "comments": 15
    },
    {
        "id": 3,
        "author": "Dr. Ananya (Agri Vet)",
        "avatar": "https://api.dicebear.com/7.x/avataaars/svg?seed=Ananya",
        "time": "1 day ago",
        "title": "Beware of new Fall Armyworm spread!",
        "content": "Farmers in the Southern region, please keep an eye out for Fall Armyworm in Maize crops. Use Neem oil spray as a preventive measure.",
        "tags": ["Alert", "Pest", "Maize"],
        "likes": 89,
        "comments": 22
    }
]


@community_bp.route('/posts', methods=['GET'])
def get_posts():
    return jsonify(POSTS)
