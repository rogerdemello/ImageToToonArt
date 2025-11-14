# 🛠️ Development Guide

<div align="center">

**Complete guide for developers contributing to the Image to Cartoon Converter**

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![React](https://img.shields.io/badge/React-18.0+-61dafb.svg)](https://reactjs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com/)

[Setup](#-development-setup) • [Architecture](#-architecture) • [Adding Features](#-adding-features) • [Testing](#-testing) • [Deployment](#-deployment)

</div>

---

## 🚀 Development Setup

### Prerequisites

| Tool | Version | Purpose |
|------|---------|----------|
| Python | 3.8+ | Backend development |
| Node.js | 14+ | Frontend development |
| Git | Latest | Version control |
| VS Code | Latest | Recommended IDE |

### Quick Setup

```bash
# Clone repository
git clone https://github.com/yourusername/ImageToToonArt.git
cd ImageToToonArt

# Run automated setup
# Windows:
setup.bat
# Linux/Mac:
chmod +x setup.sh && ./setup.sh
```

### Development Tools

#### VS Code Extensions

```json
{
  "recommendations": [
    "ms-python.python",
    "ms-python.vscode-pylance",
    "dsznajder.es7-react-js-snippets",
    "esbenp.prettier-vscode",
    "dbaeumer.vscode-eslint"
  ]
}
```

#### Dev Dependencies

**Backend:**
```bash
pip install black flake8 pytest pytest-cov mypy
```

**Frontend:**
```bash
cd frontend
npm install --save-dev eslint prettier eslint-config-prettier
```

---

## Project Architecture

### Backend Architecture

```
backend/
├── app.py                  # FastAPI routes and configuration
├── cartoon_converter.py    # Image processing logic (OpenCV)
├── ai_converter.py         # AI/ML models (PyTorch)
└── utils.py               # Helper functions
```

**Key Design Patterns:**
- **Separation of Concerns**: Converters are separate from API logic
- **Dependency Injection**: Converters initialized at startup
- **Error Handling**: Comprehensive try/except blocks
- **Validation**: Input validation before processing

### Frontend Architecture

```
frontend/src/
├── App.js         # Main component
├── App.css        # Styling
└── index.js       # Entry point
```

**State Management:**
- React hooks (useState, useCallback)
- Local component state
- No global state management (simple app)

---

## Adding New Cartoon Styles

### Option 1: Add OpenCV-based Style

**1. Add to `cartoon_converter.py`:**

```python
def _new_style_cartoon(self, image: np.ndarray) -> np.ndarray:
    """
    Your new cartoon style
    """
    # Your image processing logic here
    smooth = cv2.bilateralFilter(image, d=9, sigmaColor=75, sigmaSpace=75)
    
    # Add more processing...
    
    return processed_image
```

**2. Update `convert` method:**

```python
def convert(self, image: np.ndarray, style: str = 'classic') -> np.ndarray:
    # ... existing code ...
    elif style == 'new_style':
        return self._new_style_cartoon(image)
```

**3. Update `get_available_styles`:**

```python
def get_available_styles(self) -> list:
    return ['classic', 'smooth', 'edge_heavy', 'pencil_sketch', 
            'pencil_sketch_color', 'oil_painting', 'new_style']
```

**4. Add to frontend `STYLES` object in `App.js`:**

```javascript
new_style: {
    name: 'New Style',
    description: 'Description of your new style',
    emoji: '🎨'
}
```

### Option 2: Add AI-based Style

**1. Add to `ai_converter.py`:**

```python
def convert_new_ai_style(self, image: np.ndarray) -> np.ndarray:
    """
    New AI-based style
    """
    # Your AI model logic here
    # Can use PyTorch, TensorFlow, or other ML frameworks
    
    return styled_image
```

**2. Update `apply_neural_style_transfer`:**

```python
def apply_neural_style_transfer(self, content_image: np.ndarray, 
                                style: str = 'cartoon') -> np.ndarray:
    # ... existing code ...
    elif style == 'new_ai_style':
        return self.convert_new_ai_style(content_image)
```

**3. Update backend routes in `app.py`:**

```python
@app.post("/api/convert")
async def convert_image(...):
    # ... existing code ...
    elif style in ['cartoon', 'anime', 'watercolor', 'new_ai_style']:
        result = ai_converter.apply_neural_style_transfer(image, style)
```

---

## Adding New API Endpoints

### Example: Add Image Info Endpoint

**1. Add to `backend/app.py`:**

```python
@app.post("/api/image-info")
async def get_image_info(file: UploadFile = File(...)):
    """
    Get information about uploaded image
    """
    contents = await file.read()
    image = read_image_from_bytes(contents)
    
    height, width, channels = image.shape
    
    return {
        "filename": file.filename,
        "width": width,
        "height": height,
        "channels": channels,
        "size_bytes": len(contents)
    }
```

**2. Add frontend service function:**

```javascript
// In App.js or separate service file
const getImageInfo = async (file) => {
    const formData = new FormData();
    formData.append('file', file);
    
    const response = await axios.post(
        `${BACKEND_URL}/api/image-info`,
        formData
    );
    
    return response.data;
};
```

---

## Customizing Image Processing

### Adjusting Cartoon Parameters

**In `cartoon_converter.py`, modify `default_params`:**

```python
self.default_params = {
    'bilateral_d': 9,              # Diameter - increase for more smoothing
    'bilateral_sigma_color': 300,  # Color variance - higher = more colors merged
    'bilateral_sigma_space': 300,  # Space variance
    'median_blur_kernel': 7,       # Must be odd number
    'edge_block_size': 9,          # Edge detection sensitivity
    'edge_c': 2,                   # Edge threshold adjustment
    'color_clusters': 8            # Number of colors (lower = more cartoonish)
}
```

### Adding Configurable Parameters

**1. Modify API endpoint:**

```python
@app.post("/api/convert-advanced")
async def convert_image_advanced(
    file: UploadFile = File(...),
    style: str = Form(default="classic"),
    color_clusters: int = Form(default=8),
    edge_sensitivity: int = Form(default=2)
):
    # Use parameters in conversion
    converter = CartoonConverter()
    converter.default_params['color_clusters'] = color_clusters
    converter.default_params['edge_c'] = edge_sensitivity
    
    result = converter.convert(image, style)
    # ...
```

**2. Add UI controls in frontend:**

```javascript
const [colorClusters, setColorClusters] = useState(8);
const [edgeSensitivity, setEdgeSensitivity] = useState(2);

// Add sliders to UI
<input 
    type="range" 
    min="4" 
    max="16" 
    value={colorClusters}
    onChange={(e) => setColorClusters(e.target.value)}
/>
```

---

## Testing

### Backend Testing

**Create `backend/test_converters.py`:**

```python
import pytest
import numpy as np
from cartoon_converter import CartoonConverter
from ai_converter import AICartoonConverter

def test_classic_conversion():
    converter = CartoonConverter()
    test_image = np.zeros((100, 100, 3), dtype=np.uint8)
    result = converter.convert(test_image, 'classic')
    
    assert result is not None
    assert result.shape == test_image.shape

def test_all_styles():
    converter = CartoonConverter()
    test_image = np.random.randint(0, 255, (100, 100, 3), dtype=np.uint8)
    
    for style in converter.get_available_styles():
        result = converter.convert(test_image, style)
        assert result is not None

# Run with: pytest backend/test_converters.py
```

### API Testing

**Using pytest and httpx:**

```python
from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_styles_endpoint():
    response = client.get("/api/styles")
    assert response.status_code == 200
    assert "classic_styles" in response.json()
```

### Frontend Testing

**Create `frontend/src/App.test.js`:**

```javascript
import { render, screen } from '@testing-library/react';
import App from './App';

test('renders upload section', () => {
    render(<App />);
    const uploadText = screen.getByText(/drag & drop/i);
    expect(uploadText).toBeInTheDocument();
});
```

---

## Performance Optimization

### Backend Optimizations

**1. Image Caching:**

```python
from functools import lru_cache
import hashlib

@lru_cache(maxsize=100)
def process_cached(image_hash, style):
    # Process and return result
    pass

# In endpoint:
image_hash = hashlib.md5(image.tobytes()).hexdigest()
result = process_cached(image_hash, style)
```

**2. Async Processing:**

```python
from fastapi import BackgroundTasks

async def process_in_background(file_path, style):
    # Long-running processing
    pass

@app.post("/api/convert-async")
async def convert_async(background_tasks: BackgroundTasks, ...):
    # Save file
    background_tasks.add_task(process_in_background, path, style)
    return {"status": "processing", "task_id": "..."}
```

**3. GPU Acceleration:**

```python
# In ai_converter.py
import torch

class AICartoonConverter:
    def __init__(self):
        self.device = torch.device(
            'cuda' if torch.cuda.is_available() else 'cpu'
        )
        # Move models to GPU
        self.model.to(self.device)
```

### Frontend Optimizations

**1. Lazy Loading:**

```javascript
import React, { lazy, Suspense } from 'react';

const ImageProcessor = lazy(() => import('./ImageProcessor'));

function App() {
    return (
        <Suspense fallback={<div>Loading...</div>}>
            <ImageProcessor />
        </Suspense>
    );
}
```

**2. Image Compression:**

```javascript
const compressImage = async (file) => {
    // Use canvas to compress
    const canvas = document.createElement('canvas');
    const ctx = canvas.getContext('2d');
    // ... compression logic
};
```

---

## Deployment

### Backend Deployment

**Using Docker:**

```dockerfile
# Dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/ ./backend/

EXPOSE 8000

CMD ["uvicorn", "backend.app:app", "--host", "0.0.0.0", "--port", "8000"]
```

**Using Gunicorn (Production):**

```bash
pip install gunicorn
gunicorn backend.app:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### Frontend Deployment

**Build for Production:**

```bash
cd frontend
npm run build
```

**Serve Static Files:**

```python
# In app.py
from fastapi.staticfiles import StaticFiles

app.mount("/", StaticFiles(directory="../frontend/build", html=True))
```

---

## Environment Variables

**Create `.env` file:**

```bash
# Backend
API_PORT=8000
MAX_FILE_SIZE=10485760
ENABLE_AI=true
GPU_ENABLED=true

# Frontend
REACT_APP_BACKEND_URL=http://localhost:8000
REACT_APP_MAX_FILE_SIZE=10
```

**Load in backend:**

```python
from dotenv import load_dotenv
import os

load_dotenv()

PORT = int(os.getenv('API_PORT', 8000))
MAX_FILE_SIZE = int(os.getenv('MAX_FILE_SIZE', 10485760))
```

---

## Contributing

### Code Style

**Python (PEP 8):**
```bash
# Format code
black backend/

# Check style
flake8 backend/
```

**JavaScript (Prettier):**
```bash
# Format code
cd frontend
npx prettier --write src/
```

### Git Workflow

```bash
# Create feature branch
git checkout -b feature/new-style

# Make changes
git add .
git commit -m "Add new cartoon style"

# Push and create PR
git push origin feature/new-style
```

---

## Debugging

### Backend Debugging

**Add debug logging:**

```python
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# In functions:
logger.debug(f"Processing image with shape: {image.shape}")
```

**VS Code Debug Config (`.vscode/launch.json`):**

```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: FastAPI",
            "type": "python",
            "request": "launch",
            "module": "uvicorn",
            "args": [
                "backend.app:app",
                "--reload"
            ]
        }
    ]
}
```

### Frontend Debugging

**Browser DevTools:**
- Press F12
- Console tab for errors
- Network tab for API calls
- React DevTools extension

**Add debug output:**

```javascript
const handleConvert = async () => {
    console.log('Converting with style:', selectedStyle);
    console.log('File:', selectedFile);
    // ...
};
```

---

## Resources

### Documentation
- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [OpenCV Tutorials](https://docs.opencv.org/master/d9/df8/tutorial_root.html)
- [PyTorch Tutorials](https://pytorch.org/tutorials/)
- [React Docs](https://react.dev/)

### Learning
- Image Processing with OpenCV
- Neural Style Transfer
- REST API Design
- React Best Practices

---

## Common Development Tasks

### Add New Dependency

**Python:**
```bash
pip install new-package
pip freeze > requirements.txt
```

**Frontend:**
```bash
cd frontend
npm install new-package
```

### Update Documentation

After changes, update:
- README.md (main documentation)
- API_DOCUMENTATION.md (API changes)
- STRUCTURE.md (architecture changes)
- This file (development changes)

---

**Happy Coding! 🚀**
