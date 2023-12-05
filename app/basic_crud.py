from flask import Flask, url_for

from app.routes.auth_routes import auth_routes
from app.routes.product_routes import product_routes
from app.utilities.mysql_connection_utility import connect_to_mysql


app: Flask = Flask(__name__, template_folder='./templates/')
with app.test_request_context():
    static_url = url_for('static', filename='./resources/css/style.css')
    print(f"Generated static URL: {static_url}")

print(type(app))
print("base_crud_app")

# connection_pool = connect_to_mysql()

app.register_blueprint(auth_routes, url_prefix='/auth')
app.register_blueprint(product_routes, url_prefix='/product')

