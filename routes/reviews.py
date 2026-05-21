from flask import Blueprint, jsonify, request
from config.firebase import db
from firebase_admin import firestore

reviews_bp = Blueprint('reviews', __name__)

@reviews_bp.route("/reviews", methods=["GET"])
def get_reviews():
    if db is None:
        return jsonify({"error": "База данных недоступна"}), 500
    try:
        reviews_ref = db.collection("reviews").order_by("created_at", direction=firestore.Query.DESCENDING).stream()
        reviews_list = []
        for doc in reviews_ref:
            r = doc.to_dict()
            r["id"] = doc.id
            if "created_at" in r and r["created_at"]:
                r["created_at"] = r["created_at"].isoformat()
            reviews_list.append(r)
        return jsonify(reviews_list), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@reviews_bp.route("/reviews", methods=["POST"])
def add_review():
    if db is None:
        return jsonify({"error": "База данных недоступна"}), 500
    
    data = request.json
    if not data or "name" not in data or "text" not in data:
        return jsonify({"error": "Имя и текст отзыва обязательны"}), 400

    try:
        new_review = {
            "name": data["name"],
            "rating": data.get("rating", 5),
            "text": data["text"],
            "created_at": firestore.SERVER_TIMESTAMP
        }
        db.collection("reviews").add(new_review)
        return jsonify({"success": True}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500