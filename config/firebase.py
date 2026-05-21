import os
import firebase_admin
from firebase_admin import credentials, firestore

CONFIG_FILE = "firebase-config.json"
db = None

if not os.path.exists(CONFIG_FILE):
    print(f"Файл {CONFIG_FILE} не найден!")
else:
    try:
        cred = credentials.Certificate(CONFIG_FILE)
        firebase_admin.initialize_app(cred)
        db = firestore.client()
        print("Успешное подключение к Firebase Firestore!")
    except Exception as e:
        print(f"Ошибка инициализации Firebase: {e}")