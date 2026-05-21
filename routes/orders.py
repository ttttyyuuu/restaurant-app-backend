from flask import Blueprint, jsonify, request
from config.firebase import db
from firebase_admin import firestore

orders_bp = Blueprint('orders', __name__)

@orders_bp.route("/orders", methods=["POST"])
def create_order():
    if db is None:
        return jsonify({"error": "База данных недоступна"}), 500
    
    data = request.json
    if not data or "customer" not in data or "items" not in data:
        return jsonify({"error": "Неполные данные заказа."}), 400

    try:
        new_order = {
            "customer": data["customer"],
            "items": data["items"],
            "total": data.get("total", 0),
            "userId": data.get("userId"),
            "status": "Новый",
            "created_at": firestore.SERVER_TIMESTAMP
        }
        _, doc_ref = db.collection("orders").add(new_order)
        print(f"Получен новый заказ! ID в Firebase: {doc_ref.id}")
        return jsonify({"success": True, "order_id": doc_ref.id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@orders_bp.route("/orders", methods=["GET"])
def get_orders():
    if db is None:
        return jsonify({"error": "База данных недоступна"}), 500

    try:
        user_id = request.args.get("userId")
        orders_ref = db.collection("orders")

        if user_id:
            query = orders_ref.where(filter=firestore.FieldFilter("userId", "==", user_id))
            docs = query.stream()
        else:
            docs = orders_ref.stream()

        orders_list = []
        for doc in docs:
            order_data = doc.to_dict()
            order_data["id"] = doc.id
            if "created_at" in order_data and order_data["created_at"]:
                try:
                    order_data["created_at"] = order_data["created_at"].isoformat()
                except AttributeError:
                    order_data["created_at"] = str(order_data["created_at"])
            orders_list.append(order_data)

        return jsonify(orders_list), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500