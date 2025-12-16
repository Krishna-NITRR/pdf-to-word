# app.py
# Backend logic for PDF to Word Converter
# Tech: Flask + pdf2docx

from flask import Flask, request, send_file, jsonify
from pdf2docx import Converter
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'outputs'

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.route('/convert', methods=['POST'])
def convert_pdf_to_word():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if not file.filename.lower().endswith('.pdf'):
        return jsonify({'error': 'Only PDF files are allowed'}), 400

    filename = secure_filename(file.filename)
    pdf_path = os.path.join(UPLOAD_FOLDER, filename)
    docx_filename = filename.replace('.pdf', '.docx')
    docx_path = os.path.join(OUTPUT_FOLDER, docx_filename)

    file.save(pdf_path)

    try:
        cv = Converter(pdf_path)
        cv.convert(docx_path, start=0, end=None)
        cv.close()
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    return send_file(docx_path, as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True)
