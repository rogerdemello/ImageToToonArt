# 🎨 Image to Cartoon Converter

<div align="center">

**Transform real photos into stunning cartoon artwork using AI and image processing**

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-18.0+-61dafb.svg)](https://reactjs.org/)
[![OpenCV](https://img.shields.io/badge/OpenCV-4.8+-red.svg)](https://opencv.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

[Features](#-features) • [Demo](#-quick-start) • [Installation](#-installation) • [Usage](#-usage) • [API](#-api-reference) • [Contributing](#-contributing)

</div>

---

## ✨ Features

<table>
<tr>
<td width="50%">

### 🎨 **10 Unique Styles**
- 💎 Ultra Quality (NEW!)
- 🎨 Classic Cartoon
- ✨ Smooth Cartoon
- 🖊️ Bold Edges
- ✏️ Pencil Sketch
- 🖍️ Colored Pencil
- 🖼️ Oil Painting
- 🤖 AI Cartoon*
- 🎌 Anime Style*
- 💧 Watercolor*

<sub>*Requires PyTorch</sub>

</td>
<td width="50%">

### ⚡ **Core Features**
- 🌐 Modern web interface
- 📤 Drag & drop upload
- 🔄 Real-time processing
- 📊 Before/after comparison
- 💾 High-quality downloads
- 🚀 REST API
- 📱 Responsive design
- 🔒 Client-side preview

</td>
</tr>
</table>

## 🚀 Quick Start

### Prerequisites

| Requirement | Version | Download |
|------------|---------|----------|
| Python | 3.8+ | [Download](https://www.python.org/downloads/) |
| Node.js | 14+ | [Download](https://nodejs.org/) |
| pip | Latest | Included with Python |

### Installation

#### Option 1: Automated Setup (Recommended)

**Windows:**
```bash
setup.bat
```

**Linux/Mac:**
```bash
chmod +x setup.sh && ./setup.sh
```

#### Option 2: Manual Installation

```bash
# Clone repository
git clone https://github.com/yourusername/ImageToToonArt.git
cd ImageToToonArt

# Python setup
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Frontend setup
cd frontend
npm install
cd ..
```

### Running the Application

#### Terminal 1 - Backend
```bash
cd backend
python app.py
```
> 🌐 API: http://localhost:8000  
> 📚 Docs: http://localhost:8000/docs

#### Terminal 2 - Frontend
```bash
cd frontend
npm start
```
> 🎨 Web App: http://localhost:3000

## 💡 Usage

### Web Interface

1. **Upload** - Drag & drop or click to select image (max 10MB)
2. **Choose Style** - Select from 10 unique cartoon effects
3. **Convert** - Click convert and wait 5-30 seconds
4. **Download** - Save your cartoonized masterpiece

### API Usage

**Python Example:**
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

**cURL Example:**
```bash
curl -X POST "http://localhost:8000/api/convert" \
  -F "file=@photo.jpg" \
  -F "style=ultra" \
  --output cartoon.jpg
```

**JavaScript Example:**
```javascript
const formData = new FormData();
formData.append('file', fileInput.files[0]);
formData.append('style', 'ultra');

const response = await fetch('http://localhost:8000/api/convert', {
  method: 'POST',
  body: formData
});

const blob = await response.blob();
const url = URL.createObjectURL(blob);
```

## 🛠️ Technology Stack

<table>
<tr>
<td width="50%" valign="top">

### Backend

| Technology | Purpose |
|-----------|----------|
| **FastAPI** | REST API framework |
| **OpenCV** | Image processing |
| **PyTorch** | Deep learning (optional) |
| **NumPy** | Numerical operations |
| **Pillow** | Image I/O |
| **Uvicorn** | ASGI server |

</td>
<td width="50%" valign="top">

### Frontend

| Technology | Purpose |
|-----------|----------|
| **React 18** | UI framework |
| **Axios** | HTTP client |
| **react-dropzone** | File upload |
| **CSS3** | Styling & animations |

</td>
</tr>
</table>

## 📂 Project Structure

```
ImageToToonArt/
│
├── 📁 backend/                 # Python FastAPI Server
│   ├── app.py                 # Main API with 7 endpoints
│   ├── cartoon_converter.py   # 7 OpenCV-based styles
│   ├── ai_converter.py        # 3 AI-based styles (optional)
│   └── utils.py               # Helper functions
│
├── 📁 frontend/                # React Web Application  
│   ├── public/index.html      # HTML template
│   ├── src/
│   │   ├── App.js             # Main component with 10 styles
│   │   ├── App.css            # Modern styling
│   │   └── index.js           # Entry point
│   ├── package.json           # Dependencies
│   └── .env                   # Backend URL config
│
├── 📁 uploads/                 # Temporary uploads (.gitkeep)
├── 📁 outputs/                 # Processed images (.gitkeep)
├── 📁 models/                  # AI models (.gitkeep)
├── 📁 examples/                # Testing guide & samples
│
├── 📄 README.md                # This file
├── 📄 QUICKSTART.md            # 5-minute setup guide
├── 📄 API_DOCUMENTATION.md     # Complete API reference
├── 📄 DEVELOPMENT.md           # Developer guide
├── 📄 requirements.txt         # Python dependencies
├── 📄 setup.sh / setup.bat     # Automated installation
├── 📄 test_installation.py     # Verify setup
├── 📄 .gitignore               # Git ignore rules
└── 📄 LICENSE                  # MIT License
```

## 🎨 Style Guide

### Image Processing Styles (Fast)

| Style | Description | Processing Time | Best For |
|-------|-------------|----------------|----------|
| 💎 **Ultra Quality** | Professional-grade with advanced techniques | 10-30s | Best overall results |
| 🎨 **Classic** | Balanced edges and colors | 2-5s | General use, portraits |
| ✨ **Smooth** | Softer appearance | 3-7s | Detailed photos |
| 🖊️ **Bold Edges** | Comic book style | 2-5s | Architecture, comics |
| ✏️ **Pencil Sketch** | B&W drawing effect | 2-4s | Artistic portraits |
| 🖍️ **Colored Pencil** | Color sketch | 2-4s | Artistic color |
| 🖼️ **Oil Painting** | Painterly effect | 3-6s | Landscapes |

### AI Styles (Slower, Requires PyTorch)

| Style | Description | Processing Time | Best For |
|-------|-------------|----------------|----------|
| 🤖 **AI Cartoon** | Enhanced cartoon | 5-15s | High quality |
| 🎌 **Anime** | Japanese animation | 5-20s | Character art |
| 💧 **Watercolor** | Painting effect | 5-15s | Soft images |

### Processing Techniques

**Ultra Quality Style includes:**
- Advanced denoising with non-local means
- Triple bilateral filtering
- Multi-method edge detection (Sobel + Adaptive + Canny)
- 16-color K-means clustering
- LAB & HSV color space enhancement
- Unsharp masking
- CLAHE contrast enhancement

## 🔌 API Reference

### Endpoints

#### `GET /`
API information and status

#### `GET /health`
Health check
```json
{"status": "healthy", "converters": {...}}
```

#### `GET /api/styles`
List all available styles
```json
{"classic_styles": [...], "ai_styles": [...]}
```

#### `POST /api/convert`
Convert image to cartoon

**Parameters:**
- `file` (required): Image file
- `style` (optional): Style name (default: "ultra")
- `resize_output` (optional): Auto-resize (default: true)

**Response:** JPEG image

#### `POST /api/batch-convert`
Convert multiple images (max 10)

#### `GET /api/stats`
Get API statistics

#### `DELETE /api/cleanup`
Clean temporary files

**📚 Full API Documentation:** http://localhost:8000/docs

## 🧪 Testing

```bash
# Verify installation
python test_installation.py

# All tests should pass:
# ✅ Package Imports
# ✅ Directory Structure
# ✅ Converter Modules
# ✅ Sample Conversion
```

## 📊 Performance

| Metric | Value |
|--------|-------|
| Max File Size | 10 MB |
| Max Dimensions | 10,000 × 10,000 px |
| Auto-resize | 1920 × 1080 px |
| Ultra Quality | 10-30 seconds |
| Classic Styles | 2-7 seconds |
| API Response | < 100ms |

## 🐛 Troubleshooting

<details>
<summary><b>Backend won't start</b></summary>

```bash
# Check if port 8000 is in use
# Solution: Change port in backend/app.py or kill process
lsof -ti:8000 | xargs kill -9  # Unix
```
</details>

<details>
<summary><b>Frontend can't connect</b></summary>

1. Ensure backend is running at :8000
2. Check `frontend/.env` has correct URL
3. Verify CORS settings
</details>

<details>
<summary><b>Import errors</b></summary>

```bash
# Activate virtual environment
source venv/bin/activate  # or venv\Scripts\activate
pip install -r requirements.txt
```
</details>

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Development Setup

See [DEVELOPMENT.md](DEVELOPMENT.md) for detailed development guidelines.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [OpenCV](https://opencv.org/) - Computer vision library
- [FastAPI](https://fastapi.tiangolo.com/) - Modern web framework
- [React](https://reactjs.org/) - UI framework
- [PyTorch](https://pytorch.org/) - Deep learning platform

## 📞 Support

- 🚀 [Quick Start Guide](QUICKSTART.md) - Get running in 5 minutes
- 📚 [API Documentation](API_DOCUMENTATION.md) - Complete API reference
- 💻 [Development Guide](DEVELOPMENT.md) - Contributing & customization

---

<div align="center">

**⭐ Star this repo if you find it helpful!**

Made with ❤️ using React, FastAPI, OpenCV, and PyTorch

</div>
