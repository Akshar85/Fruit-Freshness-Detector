from flask import Flask, render_template, request, send_file, jsonify
from utils.api_client import analyze_image, generate_pdf_report, get_supported_languages
from utils.camera import capture_image
from PIL import Image
import os
import json
from werkzeug.utils import secure_filename

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
REPORTS_FOLDER = "reports"

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

if not os.path.exists(REPORTS_FOLDER):
    os.makedirs(REPORTS_FOLDER)

app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/")
def home():
    languages = get_supported_languages()
    return render_template("index.html", languages=languages)

@app.route("/api/languages")
def get_languages():
    """API endpoint to get supported languages"""
    languages = get_supported_languages()
    return jsonify(languages)

@app.route("/upload", methods=["POST"])
def upload():
    try:
        if "file" not in request.files:
            return render_template("index.html", result="Error: No file uploaded.", languages=get_supported_languages())

        file = request.files["file"]
        if file.filename == "":
            return render_template("index.html", result="Error: No selected file.", languages=get_supported_languages())
        
        if not allowed_file(file.filename):
            return render_template("index.html", result="Error: Only image files are allowed (png, jpg, jpeg, gif).", languages=get_supported_languages())

        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)

        language = request.form.get('language', 'en')
        result = analyze_image(filepath, language)
        
        return render_template("index.html", result=result, languages=get_supported_languages(), last_image=filepath)
    
    except Exception as e:
        return render_template("index.html", result=f"Error: {str(e)}", languages=get_supported_languages())

@app.route("/capture")
def capture():
    try:
        filepath = capture_image()
        language = request.args.get('language', 'en')
        result = analyze_image(filepath, language)
        return render_template("index.html", result=result, languages=get_supported_languages(), last_image=filepath)
    
    except Exception as e:
        return render_template("index.html", result=f"Error: {str(e)}", languages=get_supported_languages())

@app.route("/download-report", methods=["POST"])
def download_report():
    """Generate and download PDF report"""
    try:
        data = request.json
        image_path = data.get('image_path', '')
        result = data.get('result', '')
        
        if not image_path or not os.path.exists(image_path):
            return jsonify({"error": "Image not found"}), 400
        
        # Generate report filename
        report_filename = f"report_{os.path.splitext(os.path.basename(image_path))[0]}.pdf"
        report_path = os.path.join(REPORTS_FOLDER, report_filename)
        
        # Generate PDF
        success = generate_pdf_report(image_path, result, report_path)
        
        if success and os.path.exists(report_path):
            return send_file(report_path, as_attachment=True, download_name=report_filename)
        else:
            return jsonify({"error": "Failed to generate report"}), 500
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, host='127.0.0.1', port=5000)
