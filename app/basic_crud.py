from flask import Flask, url_for, jsonify
import os
from werkzeug.exceptions import HTTPException

from app.routes.auth_routes import auth_routes
from app.routes.product_routes import product_routes
from app.routes.upload_file_routes import upload_file_routes
# from app.routes.google_auth_route import google_auth_routes

app: Flask = Flask(__name__, template_folder='./templates/')

# Get the absolute path of the current directory
base_dir = os.path.abspath(os.path.dirname(__file__))
print(base_dir)

# Specify the relative path to the uploads folder
upload_folder = os.path.join(base_dir, 'uploads')

# Ensure the directory exists
os.makedirs(upload_folder, exist_ok=True)

app.config['UPLOAD_FOLDER'] = upload_folder
app.config['MAX_CONTENT_LENGTH'] = 10 * 1000 * 1000


with app.test_request_context():
    static_url = url_for('static', filename='./resources/css/style.css')
    print(f"Generated static URL: {static_url}")

print("base_crud_app")


@app.errorhandler(Exception)
def handle_exception(e):
    # pass through HTTP errors
    if isinstance(e, HTTPException):
        return e

    # now you're handling non-HTTP exceptions only
    return jsonify({'message': 'Internal Server error'}), 500

app.register_blueprint(auth_routes, url_prefix='/auth')
app.register_blueprint(product_routes, url_prefix='/product')
app.register_blueprint(upload_file_routes, url_prefix='/file')
# app.register_blueprint(google_auth_routes, url_prefix='/google')

