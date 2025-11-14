# 🎯 Getting Started with Image to Cartoon Converter

Welcome! This guide will walk you through everything you need to know to start converting images to cartoon style.

## Table of Contents

1. [Installation](#installation)
2. [First Run](#first-run)
3. [Using the Web Interface](#using-the-web-interface)
4. [Using the API](#using-the-api)
5. [Understanding Styles](#understanding-styles)
6. [Tips & Best Practices](#tips--best-practices)
7. [Troubleshooting](#troubleshooting)

---

## Installation

### Quick Install (Recommended)

**Windows:**
```bash
# Run the automated setup script
setup.bat
```

**Linux/Mac:**
```bash
# Make the script executable
chmod +x setup.sh

# Run the setup
./setup.sh
```

### Manual Install

If the automated script doesn't work, follow these steps:

**1. Install Python Dependencies**
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install packages
pip install -r requirements.txt
```

**2. Install Frontend Dependencies**
```bash
cd frontend
npm install
cd ..
```

**3. Verify Installation**
```bash
python test_installation.py
```

---

## First Run

### Start the Backend

```bash
# Navigate to backend directory
cd backend

# Run the server
python app.py
```

You should see:
```
🎨 Starting Image to Cartoon Converter API...
📍 Server will be available at: http://localhost:8000
INFO:     Started server process
INFO:     Uvicorn running on http://0.0.0.0:8000
```

**Keep this terminal running!**

### Start the Frontend

Open a **NEW terminal** window:

```bash
# Navigate to frontend directory
cd frontend

# Start React app
npm start
```

The browser should automatically open to `http://localhost:3000`

If not, manually navigate to: **http://localhost:3000**

---

## Using the Web Interface

### Step 1: Upload an Image

**Method 1: Drag & Drop**
- Drag an image file from your computer
- Drop it onto the upload area

**Method 2: Click to Browse**
- Click anywhere in the upload area
- Select an image from your file browser

**Supported Formats:** PNG, JPG, JPEG, GIF, BMP, WEBP

### Step 2: Choose a Style

Click on any of the 9 available styles:

**Quick Styles (Fast):**
- 🎨 Classic Cartoon - Great for general use
- ✨ Smooth Cartoon - Softer appearance
- 🖊️ Bold Edges - Comic book style

**Artistic Styles:**
- ✏️ Pencil Sketch - Black & white
- 🖍️ Colored Pencil - Color sketch
- 🖼️ Oil Painting - Painterly effect

**AI Styles (Slower):**
- 🤖 AI Cartoon - Enhanced version
- 🎌 Anime - Japanese animation
- 💧 Watercolor - Painting style

### Step 3: Convert

1. Click the **"✨ Convert to Cartoon"** button
2. Wait for processing (5-30 seconds depending on style)
3. View your before/after comparison

### Step 4: Download

- Click **"📥 Download Cartoon Image"**
- Your cartoonized image will be saved
- Click **"🔄 Convert Another Image"** to try again

---

## Using the API

### Basic Example (Python)

```python
import requests

# Upload and convert
with open('my_photo.jpg', 'rb') as f:
    files = {'file': f}
    data = {'style': 'classic'}
    
    response = requests.post(
        'http://localhost:8000/api/convert',
        files=files,
        data=data
    )

# Save result
if response.status_code == 200:
    with open('cartoon.jpg', 'wb') as f:
        f.write(response.content)
    print("Success! Saved to cartoon.jpg")
```

### Basic Example (JavaScript)

```javascript
const formData = new FormData();
formData.append('file', fileInput.files[0]);
formData.append('style', 'anime');

const response = await fetch('http://localhost:8000/api/convert', {
    method: 'POST',
    body: formData
});

const blob = await response.blob();
const url = URL.createObjectURL(blob);
// Use url to display or download
```

### Using curl

```bash
curl -X POST "http://localhost:8000/api/convert" \
  -F "file=@photo.jpg" \
  -F "style=anime" \
  --output result.jpg
```

---

## Understanding Styles

### When to Use Each Style

| Style | Best For | Processing Speed | Details |
|-------|----------|------------------|---------|
| Classic Cartoon | Portraits, landscapes, general use | ⚡ Fast | Balanced, versatile |
| Smooth Cartoon | Detailed photos, textures | ⚡ Fast | Softer look |
| Bold Edges | Architecture, comics | ⚡ Fast | Strong outlines |
| Pencil Sketch | Portraits, artistic | ⚡ Fast | B&W drawing |
| Colored Pencil | Artistic portraits | ⚡ Fast | Color sketch |
| Oil Painting | Landscapes, artistic | ⚡ Medium | Painterly |
| AI Cartoon | High-quality results | 🐌 Slower | Enhanced |
| Anime | Character art, portraits | 🐌 Slower | Japanese style |
| Watercolor | Nature, soft images | 🐌 Slower | Painted look |

### Style Comparison Examples

**For a Portrait Photo:**
1. Try `classic` first (fast baseline)
2. Compare with `anime` for stylized look
3. Try `pencil_sketch` for artistic version

**For a Landscape:**
1. Start with `classic`
2. Try `watercolor` for artistic feel
3. Use `oil_painting` for painterly effect

**For Architecture:**
1. Use `edge_heavy` for strong lines
2. Try `classic` for balanced look
3. `pencil_sketch` for architectural drawing

---

## Tips & Best Practices

### Image Quality

✅ **DO:**
- Use well-lit images
- Choose high-resolution photos
- Ensure clear subjects
- Use images with good contrast

❌ **AVOID:**
- Very dark or overexposed images
- Extremely low resolution (<100x100)
- Very blurry or out-of-focus images

### Performance Tips

**For Faster Processing:**
- Use classic styles (not AI styles)
- Resize large images before upload
- Ensure backend has adequate resources

**For Best Quality:**
- Use original, high-quality images
- Try multiple styles and compare
- Use AI styles for important conversions

### Workflow Suggestions

**Batch Processing:**
```python
# Process multiple images with same style
import os
import requests

for image_file in os.listdir('my_photos/'):
    with open(f'my_photos/{image_file}', 'rb') as f:
        files = {'file': f}
        data = {'style': 'classic'}
        response = requests.post(
            'http://localhost:8000/api/convert',
            files=files, data=data
        )
        
        if response.status_code == 200:
            with open(f'results/{image_file}', 'wb') as out:
                out.write(response.content)
```

**Testing All Styles:**
```python
# Try all styles on one image
styles = ['classic', 'smooth', 'edge_heavy', 'anime', 'watercolor']

for style in styles:
    with open('photo.jpg', 'rb') as f:
        response = requests.post(
            'http://localhost:8000/api/convert',
            files={'file': f},
            data={'style': style}
        )
    
    with open(f'{style}_result.jpg', 'wb') as f:
        f.write(response.content)
```

---

## Troubleshooting

### Common Issues

**Problem: Backend won't start**
```
Error: Address already in use

Solution: Port 8000 is in use. Either:
1. Stop the other process using port 8000
2. Change the port in backend/app.py (line 343)
```

**Problem: Frontend can't connect to backend**
```
Error: Network Error

Solution:
1. Ensure backend is running (check terminal)
2. Verify backend is at http://localhost:8000
3. Check frontend/.env has correct URL
```

**Problem: Import errors in Python**
```
ModuleNotFoundError: No module named 'cv2'

Solution:
1. Activate virtual environment
2. Run: pip install -r requirements.txt
```

**Problem: Image conversion fails**
```
Error: File too large

Solution:
1. Image exceeds 10MB limit
2. Resize image before upload
3. Or compress image quality
```

**Problem: Slow processing**
```
Conversion takes too long

Solution:
1. Use classic styles instead of AI
2. Resize image to smaller dimensions
3. Check if backend has sufficient resources
```

### Getting Help

1. **Check Documentation:**
   - README.md
   - API_DOCUMENTATION.md
   - This file (GETTING_STARTED.md)

2. **Test Installation:**
   ```bash
   python test_installation.py
   ```

3. **Check Logs:**
   - Backend terminal for errors
   - Browser console (F12) for frontend errors

4. **API Documentation:**
   - Visit: http://localhost:8000/docs
   - Test endpoints interactively

---

## Next Steps

Now that you're set up:

1. **Experiment** - Try different images and styles
2. **Learn the API** - Read API_DOCUMENTATION.md
3. **Customize** - Modify styles or add new ones
4. **Build** - Create your own applications using the API

### Example Projects You Can Build

- Photo gallery with cartoon filters
- Batch image processor
- Social media cartoon avatar creator
- Animated cartoon effect generator
- Custom style training (advanced)

---

## Quick Reference

### Start Backend
```bash
cd backend && python app.py
```

### Start Frontend
```bash
cd frontend && npm start
```

### Test Installation
```bash
python test_installation.py
```

### API Test
```bash
curl http://localhost:8000/health
```

### Available Styles
```
classic, smooth, edge_heavy, pencil_sketch, 
pencil_sketch_color, oil_painting, cartoon, anime, watercolor
```

---

**Happy Converting! 🎨**

For more details, see the full documentation in README.md
