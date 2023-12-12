import os
from flask import Blueprint, current_app as app, flash, request, redirect, jsonify, send_from_directory, render_template_string
from werkzeug.utils import secure_filename
from datetime import datetime

upload_file_routes = Blueprint('upload_file_routes', __name__)

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Upload File
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
            timestamp =  datetime.now().strftime('%Y%m%d%H%M%S')

            filename = secure_filename(f"{timestamp}_{file.filename}")
            upload_folder = app.config['UPLOAD_FOLDER']
            file.save(os.path.join(upload_folder, filename))

    return jsonify({'message': 'File Uploaded Successfully!'})


# Download File
@upload_file_routes.route('/download/<string:file_name>')
def download_file(file_name):
    return send_from_directory(app.config["UPLOAD_FOLDER"], file_name)


@upload_file_routes.route('/delete-file/<string:file_name>', methods=['POST'])
def delete_file(file_name):
    try:
        upload_folder = app.config['UPLOAD_FOLDER']
        file_path = os.path.join(upload_folder, file_name)

        # Check if the file exists before attempting to remove it
        if os.path.exists(file_path):
            os.remove(file_path)
            return jsonify({'message': 'File deleted successfully'})
        else:
            return jsonify({'message': 'File not found'}), 404
            # return render_template_string('<p>File not found</p>'), 404
    except Exception as e:
        return jsonify({'message': f'Error deleting file: {str(e)}'}), 500