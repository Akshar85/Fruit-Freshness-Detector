import requests
import base64
import os
from dotenv import load_dotenv
import json
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from datetime import datetime

load_dotenv()

API_KEY = os.getenv("GOOGLE_API_KEY")

# Google Gemini Vision API endpoint - using gemini-2.5-flash which supports images
API_MODEL = "gemini-2.5-flash"
API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/{API_MODEL}:generateContent?key={API_KEY}"

# Supported languages
SUPPORTED_LANGUAGES = {
    "en": "English",
    "es": "Español",
    "fr": "Français",
    "de": "Deutsch",
    "it": "Italiano",
    "pt": "Português",
    "ru": "Русский",
    "ja": "日本語",
    "zh": "中文",
    "hi": "हिन्दी",
    "ar": "العربية",
    "ko": "한국어",
    "tr": "Türkçe",
    "pl": "Polski",
    "nl": "Nederlands",
    "sv": "Svenska",
    "th": "ไทย",
    "vi": "Tiếng Việt",
    "id": "Bahasa Indonesia",
    "el": "Ελληνικά",
    "gu": "ગુજરાતી"
}


def analyze_image(image_path, language="en"):
    """Send image to Google Gemini Vision API and return fruit identification and freshness result with confidence score"""
    
    try:
        if not os.path.exists(image_path):
            return "Analysis result: Image file not found."
        
        # Read and encode image
        with open(image_path, "rb") as f:
            image_bytes = f.read()
            encoded = base64.b64encode(image_bytes).decode()
        
        # Determine MIME type based on file extension
        ext = os.path.splitext(image_path)[1].lower()
        mime_types = {
            '.jpg': 'image/jpeg',
            '.jpeg': 'image/jpeg',
            '.png': 'image/png',
            '.gif': 'image/gif',
            '.webp': 'image/webp'
        }
        mime_type = mime_types.get(ext, 'image/jpeg')

        # Format for Gemini Vision API - asking for fruit identification and freshness with confidence
        payload = {
            "contents": [
                {
                    "parts": [
                        {
                            "text": """Analyze this image and provide:
1. Identify ALL fruits visible in the image (list each fruit type)
2. For each fruit, determine if it is FRESH or ROTTEN
3. Provide a confidence score (0-100%) for your analysis
4. Provide a brief quality assessment for each fruit

Format your response exactly like this:
Fruits Found: [list fruits]
Status: [FRESH or ROTTEN for each]
Confidence: [0-100%]
Quality: [brief assessment]

Be specific about fruit types (e.g., Apple, Banana, Orange, etc.)"""
                        },
                        {
                            "inline_data": {
                                "mime_type": mime_type,
                                "data": encoded
                            }
                        }
                    ]
                }
            ]
        }

        # Make API request
        headers = {
            "Content-Type": "application/json"
        }
        
        response = requests.post(API_URL, json=payload, headers=headers, timeout=30)

        # Check if request was successful
        if response.status_code == 200:
            data = response.json()
            
            try:
                # Extract text from response
                result_text = data["candidates"][0]["content"]["parts"][0]["text"].strip()
                
                # Process and format the response
                formatted_result = format_analysis_result(result_text)
                
                # Translate if language is not English
                if language and language != "en":
                    formatted_result = translate_text(formatted_result, language)
                
                return formatted_result
                    
            except (KeyError, IndexError, TypeError) as e:
                return f"Analysis result: Could not parse API response. Try again."
        
        elif response.status_code == 400:
            error_data = response.json()
            error_msg = error_data.get("error", {}).get("message", "Bad request")
            return f"Analysis result: Invalid request - {error_msg}"
        
        elif response.status_code == 401:
            return "Analysis result: API key is invalid. Please check your GOOGLE_API_KEY in the .env file."
        
        elif response.status_code == 403:
            return "Analysis result: API access denied. Make sure the Generative Language API is enabled."
        
        elif response.status_code == 429:
            return "Analysis result: API rate limit exceeded. Please try again later."
        
        elif response.status_code == 500:
            return "Analysis result: Server error. Please try again later."
        
        else:
            return f"Analysis result: API error (Status {response.status_code}). Please try again."
    
    except requests.exceptions.Timeout:
        return "Analysis result: Request timeout. The API took too long to respond. Please try again."
    
    except requests.exceptions.ConnectionError:
        return "Analysis result: Connection error. Please check your internet connection."
    
    except Exception as e:
        return f"Analysis result: Error - {str(e)}"


def format_analysis_result(api_response):
    """Format the API response into a user-friendly result with confidence score"""
    
    try:
        # Parse the response to extract key information
        lines = api_response.split('\n')
        
        formatted_result = "📊 <strong>Analysis Result:</strong>\n\n"
        confidence = "N/A"
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            if line.startswith("Fruits Found:") or line.startswith("Fruits found:"):
                fruits = line.replace("Fruits Found:", "").replace("Fruits found:", "").strip()
                formatted_result += f"🍎 <strong>Fruits Found:</strong> {fruits}\n\n"
            
            elif line.startswith("Status:") or line.startswith("Freshness:"):
                status = line.replace("Status:", "").replace("Freshness:", "").strip()
                
                # Add emoji based on status
                if "FRESH" in status.upper() or "GOOD" in status.upper():
                    formatted_result += f"✅ <strong>Status:</strong> {status}\n\n"
                elif "ROTTEN" in status.upper() or "BAD" in status.upper():
                    formatted_result += f"❌ <strong>Status:</strong> {status}\n\n"
                else:
                    formatted_result += f"ℹ️ <strong>Status:</strong> {status}\n\n"
            
            elif line.startswith("Confidence:"):
                confidence = line.replace("Confidence:", "").strip()
                formatted_result += f"🎯 <strong>Confidence Score:</strong> {confidence}\n\n"
            
            elif line.startswith("Quality:") or line.startswith("Assessment:"):
                quality = line.replace("Quality:", "").replace("Assessment:", "").strip()
                formatted_result += f"📝 <strong>Quality Assessment:</strong> {quality}\n"
        
        # If no special formatting was found, return the raw response with some formatting
        if formatted_result == "📊 <strong>Analysis Result:</strong>\n\n":
            formatted_result = "📊 <strong>Analysis Result:</strong>\n\n" + api_response
        
        return formatted_result
    
    except Exception as e:
        return f"Analysis result: {api_response}"


def generate_pdf_report(image_path, analysis_result, output_path):
    """Generate a PDF report of the analysis"""
    
    try:
        doc = SimpleDocTemplate(output_path, pagesize=letter)
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor='#667eea',
            spaceAfter=30,
            alignment=TA_CENTER
        )
        
        elements = []
        
        # Title
        elements.append(Paragraph("🍎 Fruit Freshness Analysis Report", title_style))
        elements.append(Spacer(1, 0.3*inch))
        
        # Date
        elements.append(Paragraph(f"<b>Analysis Date:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", styles['Normal']))
        elements.append(Spacer(1, 0.2*inch))
        
        # Image
        if os.path.exists(image_path):
            try:
                img = Image(image_path, width=4*inch, height=3*inch)
                elements.append(img)
                elements.append(Spacer(1, 0.3*inch))
            except:
                pass
        
        # Analysis Results
        elements.append(Paragraph("<b>Analysis Results:</b>", styles['Heading2']))
        elements.append(Spacer(1, 0.2*inch))
        
        # Clean up HTML tags for PDF
        clean_result = analysis_result.replace("<strong>", "").replace("</strong>", "").replace("<br>", "\n")
        elements.append(Paragraph(clean_result.replace("\n", "<br/>"), styles['Normal']))
        
        # Build PDF
        doc.build(elements)
        return True
    
    except Exception as e:
        print(f"Error generating PDF: {str(e)}")
        return False


def translate_text(text, target_language="en"):
    """Translate text to target language using MyMemory API"""
    try:
        if target_language == "en":
            return text
        
        # Use MyMemory Translation API (free, no auth required)
        url = "https://api.mymemory.translated.net/get"
        params = {
            "q": text,
            "langpair": f"en|{target_language}"
        }
        
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if data.get("responseStatus") == 200:
                translated_text = data.get("responseData", {}).get("translatedText", text)
                return translated_text
        
        # If translation fails, return original text
        return text
    
    except Exception as e:
        print(f"Translation error: {str(e)}")
        return text


def get_supported_languages():
    """Return list of supported languages"""
    return SUPPORTED_LANGUAGES
