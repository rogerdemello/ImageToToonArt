# 🚀 Quick Start Guide

Get the Image to Cartoon Converter running in under 5 minutes!

---

## 📋 Prerequisites

| Requirement | Minimum Version | Download Link |
|------------|----------------|---------------|
| **Python** | 3.8+ | [python.org/downloads](https://www.python.org/downloads/) |
| **Node.js** | 14+ | [nodejs.org](https://nodejs.org/) |
| **pip** | Latest | Included with Python |

> **💡 Tip:** Verify installations with `python --version`, `node --version`, and `npm --version`

---

## ⚡ Installation

### Option 1: Automated Setup (Recommended)

**Windows:**
```bash
setup.bat
```

**Linux/Mac:**
```bash
chmod +x setup.sh && ./setup.sh
```

### Option 2: Manual Installation

<details>
<summary><b>Click to expand manual steps</b></summary>

#### 1️⃣ Set Up Python Backend

```bash
# Navigate to project directory
cd ImageToToonArt

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

#### 2️⃣ Set Up React Frontend

```bash
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Return to root
cd ..
```

</details>

---

## 🎬 Running the Application

### Start Backend (Terminal 1)

```bash
cd backend
python app.py
```

✅ **Backend running:** http://localhost:8000  
📚 **API Docs:** http://localhost:8000/docs

### Start Frontend (Terminal 2)

```bash
cd frontend
npm start
```

✅ **Web App:** http://localhost:3000

---

## 🎯 Using the Application

### Step 1: Upload Image
- 📤 Drag & drop or click to browse
- 📁 Supported: PNG, JPG, JPEG, GIF, BMP, WEBP
- 📏 Max size: 10MB

### Step 2: Choose Style

| Style | Speed | Best For |
|-------|-------|----------|
| 💎 **Ultra Quality** | 10-30s | Best overall results |
| 🎨 **Classic** | 2-5s | General photos |
| 🖊️ **Bold Edges** | 2-5s | Comic book look |
| ✏️ **Pencil Sketch** | 2-4s | Black & white art |
| 🤖 **AI Cartoon** | 5-15s | High quality (needs PyTorch) |

### Step 3: Convert & Download
1. Click **"Convert to Cartoon"**
2. Wait for processing
3. View before/after comparison
4. Click **"Download"** to save

---

## 🧪 Testing the API

### Interactive API Documentation
Visit: http://localhost:8000/docs

### Quick API Test

**Get available styles:**
```bash
curl http://localhost:8000/api/styles
```

**Convert an image:**
```bash
curl -X POST "http://localhost:8000/api/convert" \
  -F "file=@photo.jpg" \
  -F "style=ultra" \
  --output cartoon.jpg
```

**Python example:**
```python
import requests

with open('photo.jpg', 'rb') as f:
    response = requests.post(
        'http://localhost:8000/api/convert',
        files={'file': f},
        data={'style': 'ultra'}
    )

with open('cartoon.jpg', 'wb') as f:
    f.write(response.content)
```

---

## 🐛 Troubleshooting

<details>
<summary><b>Import errors when starting backend</b></summary>

**Solution:**
```bash
# Ensure virtual environment is activated
source venv/bin/activate  # or venv\Scripts\activate
pip install -r requirements.txt
```
</details>

<details>
<summary><b>Port 8000 already in use</b></summary>

**Solution 1:** Kill existing process
```bash
# Unix/Mac
lsof -ti:8000 | xargs kill -9

# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

**Solution 2:** Change port in `backend/app.py`:
```python
uvicorn.run("app:app", host="0.0.0.0", port=8001, ...)
```
</details>

<details>
<summary><b>npm install fails</b></summary>

**Solution:**
```bash
cd frontend
rm -rf node_modules package-lock.json
npm cache clean --force
npm install
```
</details>

<details>
<summary><b>Frontend can't connect to backend</b></summary>

**Solution:**
1. Verify backend is running at :8000
2. Check `frontend/.env`:
```
REACT_APP_BACKEND_URL=http://localhost:8000
```
</details>

<details>
<summary><b>Conversion takes too long</b></summary>

**Solution:**
- Use classic styles (2-7s) instead of AI styles
- Resize large images before upload
- Close other resource-intensive apps
</details>

---

## 💡 Pro Tips

✨ **Best Practices:**
- Start with **Ultra Quality** or **Classic** style
- Use high-quality source images for best results
- Try multiple styles on the same image
- Classic styles are fastest for quick previews

🎨 **Style Recommendations:**
- **Portraits** → Ultra Quality, Classic, Anime
- **Landscapes** → Oil Painting, Watercolor
- **Architecture** → Bold Edges, Classic
- **Artistic** → Pencil Sketch, Colored Pencil

---

## 📚 Next Steps

| Resource | Description |
|----------|-------------|
| [README.md](README.md) | Full documentation & features |
| [API_DOCUMENTATION.md](API_DOCUMENTATION.md) | Complete API reference & client libraries |
| [DEVELOPMENT.md](DEVELOPMENT.md) | Contributing & adding custom styles |
| [examples/README.md](examples/README.md) | Testing guide & sample scripts |

---

## 🎉 You're Ready!

Start transforming your photos into stunning cartoon art!

**Happy converting! 🎨✨**
