from flask import Flask, url_for
import os

from app.routes.auth_routes import auth_routes
from app.routes.product_routes import product_routes
from app.routes.upload_file_routes import upload_file_routes
# from app.utilities.mysql_connection_utility import connect_to_mysql


app: Flask = Flask(__name__, template_folder='./templates/')


# Get the absolute path of the current directory
base_dir = os.path.abspath(os.path.dirname(__file__))

# Specify the relative path to the uploads folder
upload_folder = os.path.join(base_dir, 'uploads')

# Ensure the directory exists
os.makedirs(upload_folder, exist_ok=True)

app.config['UPLOAD_FOLDER'] = upload_folder


with app.test_request_context():
    static_url = url_for('static', filename='./resources/css/style.css')
    print(f"Generated static URL: {static_url}")

print(type(app))
print("base_crud_app")

# connection_pool = connect_to_mysql()

app.register_blueprint(auth_routes, url_prefix='/auth')
app.register_blueprint(product_routes, url_prefix='/product')
app.register_blueprint(upload_file_routes, url_prefix='/file')

