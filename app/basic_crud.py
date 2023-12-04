from flask import Flask

from app.routes.auth_routes import auth_routes

app: Flask = Flask(__name__, template_folder='./templates/')
print(type(app))
print("base_crud_app")

app.register_blueprint(auth_routes, url_prefix='/auth')


