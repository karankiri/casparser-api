import io
from flask import Flask, request, jsonify
from flask_cors import CORS
import casparser

app = Flask(__name__)
CORS(app)  # This enables CORS for all routes

@app.route('/parse', methods=['POST'])
def parse_pdf():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    if file and file.filename.endswith('.pdf'):
        try:
            # Read the file into a BytesIO object
            pdf_file = io.BytesIO(file.read())
            
            # Pass the BytesIO object to casparser
            data = casparser.read_cas_pdf(pdf_file, "", output="json")
            return data
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    else:
        return jsonify({"error": "Invalid file format"}), 400

if __name__ == '__main__':
    app.run(debug=True)