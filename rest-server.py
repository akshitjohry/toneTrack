from flask import Flask, request, jsonify
import base64
import os

app = Flask(__name__)

# Change the UPLOAD_FOLDER to your desired local directory path
UPLOAD_FOLDER = '/home/ajay/DSC/temp'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/upload', methods=['POST'])
def upload_file():
    data = request.get_json()

    if 'mp3' not in data or 'filename' not in data:
        return jsonify({'error': 'Invalid data format'}), 400

    mp3_data = base64.b64decode(data['mp3'])
    filename = data['filename'] + '.mp3'

    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

    with open(file_path, 'wb') as f:
        f.write(mp3_data)

    return jsonify({'message': 'File uploaded successfully'}), 200

if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

    app.run(host='0.0.0.0', port=5000)
