# Fruit Freshness Detector with Flask

A modern Flask-based web application that analyzes fruit freshness using Google's Gemini Vision AI. Features multi-language support, dark mode, confidence scoring, and PDF report generation.

## Prerequisites

- Python 3.8 or higher
- Pip (Python package manager)
- A Google API key (for Gemini Vision API access)
- Webcam (optional, for camera capture feature)

## Installation

### 1. Clone or navigate to the project directory
```bash
cd c:\CODES\Fruit-Freshness-Detector-with-Flask
```

### 2. Create a virtual environment (recommended)
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Set up your Google API key
```bash
# Copy the example file
copy .env.example .env

# Edit .env and add your Google API key
# GOOGLE_API_KEY=your_api_key_here

# You can get a free API key from: https://console.cloud.google.com/
# Enable the Generative Language API in your Google Cloud project
```

## Running the Application

```bash
# Make sure your virtual environment is activated
python main.py
```

The application will start on `http://127.0.0.1:5000`

## Features

- 📤 **Upload Image**: Upload fruit images to analyze freshness
- 📷 **Capture from Camera**: Capture live images from your webcam for analysis
- 🤖 **AI Analysis**: Uses Google's Gemini 2.5-Flash Vision API for accurate fruit detection
- 🍎 **Fruit Identification**: Identifies all fruits present in the image
- ✅ **Freshness Detection**: Determines if each fruit is FRESH or ROTTEN
- 📊 **Confidence Scores**: Provides 0-100% confidence rating for analysis accuracy
- 📝 **Quality Assessment**: Detailed quality assessment for each fruit
- 📥 **PDF Reports**: Generate and download professional PDF analysis reports
 - 🌍 **Multi-Language Support**: 20+ languages supported (English, Spanish, French, German, Chinese, Japanese, Gujarati (ગુજરાતી), and more)
- 🌙 **Dark Mode**: Toggle between light and dark themes with persistent preference
- 💾 **Responsive Design**: Works seamlessly on desktop and mobile devices

## Usage

1. Open your browser and navigate to `http://127.0.0.1:5000`
2. (Optional) Select your preferred language from the dropdown
3. Choose to either:
   - Upload an image file (PNG, JPG, JPEG, or GIF)
   - Capture an image from your webcam
4. The application will analyze the fruit and display:
   - List of identified fruits
   - Freshness status (FRESH/ROTTEN)
   - Confidence score
   - Quality assessment
5. Download the analysis as a PDF report if needed
6. Toggle dark mode using the moon/sun button in the top-right

## File Structure

```
.
├── main.py                 # Flask application entry point
├── requirements.txt        # Python dependencies
├── .env.example           # Example environment configuration
├── README.md              # This file
├── templates/
│   └── index.html         # Web interface with language selector
├── static/
│   └── style.css          # Styling with light/dark mode support
├── utils/
│   ├── api_client.py      # Google Gemini API integration & PDF generation
│   └── camera.py          # Webcam capture functionality
├── uploads/               # Uploaded/captured images directory (auto-created)
└── reports/               # Generated PDF reports directory (auto-created)
```

## API Details

### Google Gemini Vision API
- **Model**: gemini-2.5-flash
- **Capabilities**: Image analysis, fruit detection, quality assessment
- **Prompt Engineering**: Specifically trained to identify fruits and assess freshness

### Translation API
- **Service**: MyMemory Translation API (free, no authentication required)
- **Languages**: 20+ languages supported including major world languages

## Configuration

### Environment Variables (.env file)
```
GOOGLE_API_KEY=your_google_api_key_here
```

## Troubleshooting

### "No module named 'flask'" or other import errors
- Ensure your virtual environment is activated
- Run: `pip install -r requirements.txt`

### "API key is invalid"
- Verify your `.env` file has `GOOGLE_API_KEY` set correctly
- Check that the Generative Language API is enabled in Google Cloud Console
- Ensure your API key has access to Gemini models

### "Camera not available"
- Check if your webcam is connected and working
- Ensure no other application is using the camera
- Check browser permissions for camera access

