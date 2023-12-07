import os
from flask import Blueprint, current_app as app, flash, request, redirect, jsonify
from werkzeug.utils import secure_filename

upload_file_routes = Blueprint('upload_file_routes', __name__)

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@upload_file_routes.route('/upload', methods=['POST'])
def upload_file():
    with app.app_context():
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)

        file = request.files['file']

        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            upload_folder = app.config['UPLOAD_FOLDER']
            file.save(os.path.join(upload_folder, filename))

    return jsonify({'message': 'Hi'})
