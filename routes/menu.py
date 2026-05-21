from flask import Blueprint, jsonify, request
from config.firebase import db
from data.menu_data import DEFAULT_MENU

menu_bp = Blueprint('menu', __name__)

def seed_menu_if_empty():
    if db is None:
        return
    try:
        menu_ref = db.collection("menu")
        docs = menu_ref.limit(1).get()
        if len(docs) == 0:
            print("База данных пуста. Заполняю меню оригинальными блюдами...")
            for item in DEFAULT_MENU:
                menu_ref.document(str(item["id"])).set(item)
            print("Наполнение базы успешно завершено!")
    except Exception as e:
        print(f"Не удалось проверить или заполнить меню: {e}")

@menu_bp.route("/menu", methods=["GET"])
def get_menu():
    if db is None:
        return jsonify({"error": "База данных недоступна"}), 500
    try:
        seed_menu_if_empty()
        menu_ref = db.collection("menu").stream()
        menu_list = []
        base_url = request.host_url 
        
        for doc in menu_ref:
            item = doc.to_dict()
            item["image"] = f"{base_url}assets/{item['image']}"
            menu_list.append(item)
            
        menu_list.sort(key=lambda x: x.get("id", 0))
        return jsonify(menu_list), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500