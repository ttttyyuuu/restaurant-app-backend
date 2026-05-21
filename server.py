from flask import Flask
from flask_cors import CORS

# Импортируем роуты (блюпринты)
from routes.menu import menu_bp
from routes.orders import orders_bp
from routes.reviews import reviews_bp

app = Flask(__name__, static_folder="assets", static_url_path="/assets")
CORS(app)

# Регистрируем модули с общим URL-префиксом /api
app.register_blueprint(menu_bp, url_prefix='/api')
app.register_blueprint(orders_bp, url_prefix='/api')
app.register_blueprint(reviews_bp, url_prefix='/api')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)