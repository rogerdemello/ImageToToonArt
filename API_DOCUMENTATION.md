# 📖 API Documentation

Complete REST API reference for the Image to Cartoon Converter.

<div align="center">

[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-009688.svg)](https://fastapi.tiangolo.com/)
[![OpenAPI](https://img.shields.io/badge/OpenAPI-3.0-green.svg)](http://localhost:8000/docs)
[![Status](https://img.shields.io/badge/Status-Active-success.svg)]()

**Interactive Docs:** [Swagger UI](http://localhost:8000/docs) • [ReDoc](http://localhost:8000/redoc)

</div>

---

## 🔗 Base URL

```
http://localhost:8000
```

## 📡 Quick Reference

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/health` | GET | Health check |
| `/api/styles` | GET | List available styles |
| `/api/convert` | POST | Convert single image |
| `/api/batch-convert` | POST | Convert multiple images |
| `/api/stats` | GET | Usage statistics |
| `/api/cleanup` | DELETE | Remove temporary files |

---

## 🎯 Endpoints

### 1. Health Check

Check API status and availability.

**`GET /health`**

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2025-11-12T10:30:00.000000",
  "converters": {
    "classic": "available",
    "ai": "available"
  }
}
```

**Status Codes:**
- `200` - API is healthy
- `500` - API is experiencing issues

---

### 2. Get Available Styles

List all cartoon conversion styles.

**`GET /api/styles`**

**Response:**
```json
{
  "classic_styles": [
    "ultra",
    "classic", 
    "smooth",
    "edge_heavy",
    "pencil_sketch",
    "pencil_sketch_color",
    "oil_painting"
  ],
  "ai_styles": ["cartoon", "anime", "watercolor"],
  "all_styles": {
    "ultra": {
      "name": "Ultra Quality",
      "description": "Professional-grade with advanced techniques",
      "processing_time": "10-30s"
    },
    "classic": {
      "name": "Classic Cartoon",
      "description": "Edge detection with color quantization",
      "processing_time": "2-5s"
    }
    // ... more styles
  }
}
```

---

### 3. Convert Image

Transform an image into cartoon artwork.

**`POST /api/convert`**

#### Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `file` | File | ✅ Yes | - | Image file to convert |
| `style` | String | ❌ No | `ultra` | Conversion style |
| `resize_output` | Boolean | ❌ No | `true` | Auto-resize large images |

#### Supported Image Formats
- PNG, JPG, JPEG, GIF, BMP, WEBP

#### File Constraints
- **Max size:** 10 MB
- **Min dimensions:** 50 × 50 px
- **Max dimensions:** 10,000 × 10,000 px
- **Auto-resize:** Images > 1920 × 1080 px

#### Request Examples

<details>
<summary><b>cURL</b></summary>

```bash
curl -X POST "http://localhost:8000/api/convert" \
  -F "file=@photo.jpg" \
  -F "style=ultra" \
  --output cartoon.jpg
```
</details>

<details>
<summary><b>Python</b></summary>

```python
import requests

with open('photo.jpg', 'rb') as f:
    response = requests.post(
        'http://localhost:8000/api/convert',
        files={'file': f},
        data={'style': 'ultra'}
    )

if response.status_code == 200:
    with open('cartoon.jpg', 'wb') as f:
        f.write(response.content)
else:
    print(f"Error: {response.json()}")
```
</details>

<details>
<summary><b>JavaScript/Node.js</b></summary>

```javascript
const FormData = require('form-data');
const fs = require('fs');
const axios = require('axios');

const formData = new FormData();
formData.append('file', fs.createReadStream('photo.jpg'));
formData.append('style', 'ultra');

const response = await axios.post(
  'http://localhost:8000/api/convert',
  formData,
  {
    headers: formData.getHeaders(),
    responseType: 'arraybuffer'
  }
);

fs.writeFileSync('cartoon.jpg', response.data);
```
</details>

<details>
<summary><b>Browser JavaScript</b></summary>

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
</details>

#### Success Response

**Status:** `200 OK`  
**Content-Type:** `image/jpeg`

**Headers:**
```
Content-Disposition: attachment; filename="cartoon_ultra_abc123.jpg"
X-Processing-Style: ultra
X-Original-Filename: photo.jpg
X-Processing-Time: 12.34
```

#### Error Responses

<table>
<tr>
<th>Status</th>
<th>Response</th>
<th>Description</th>
</tr>
<tr>
<td><code>400</code></td>
<td>

```json
{
  "detail": "Invalid file type. Allowed: PNG, JPG, JPEG, GIF, BMP, WEBP"
}
```
</td>
<td>Unsupported file format</td>
</tr>
<tr>
<td><code>400</code></td>
<td>

```json
{
  "detail": "File size (15.50MB) exceeds maximum (10MB)"
}
```
</td>
<td>File too large</td>
</tr>
<tr>
<td><code>400</code></td>
<td>

```json
{
  "detail": "Unknown style: xyz. Use /api/styles to see available styles."
}
```
</td>
<td>Invalid style name</td>
</tr>
<tr>
<td><code>500</code></td>
<td>

```json
{
  "detail": "Error processing image: <error details>"
}
```
</td>
<td>Processing failure</td>
</tr>
</table>

---

### 4. Batch Convert Images

Process multiple images simultaneously.

**`POST /api/batch-convert`**

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `files` | File[] | ✅ Yes | Array of images (max 10) |
| `style` | String | ❌ No | Style for all images |

#### Request Example

```bash
curl -X POST "http://localhost:8000/api/batch-convert" \
  -F "files=@image1.jpg" \
  -F "files=@image2.jpg" \
  -F "files=@image3.jpg" \
  -F "style=ultra"
```

#### Response

**Status:** `200 OK`

```json
{
  "total": 3,
  "successful": 2,
  "failed": 1,
  "results": [
    {
      "filename": "image1.jpg",
      "output_filename": "cartoon_ultra_abc123.jpg",
      "status": "success",
      "style": "ultra",
      "processing_time": 12.5
    },
    {
      "filename": "image2.jpg",
      "status": "error",
      "message": "Invalid file type"
    },
    {
      "filename": "image3.jpg",
      "output_filename": "cartoon_ultra_def456.jpg",
      "status": "success",
      "style": "ultra",
      "processing_time": 15.2
    }
  ]
}
```

---

### 5. Get Statistics

Retrieve API usage statistics.

**`GET /api/stats`**

**Response:**
```json
{
  "uploads": 47,
  "outputs": 62,
  "available_styles": 10,
  "server_time": "2025-11-12T10:30:00.000000",
  "uptime": "5 hours 23 minutes"
}
```

---

### 6. Cleanup Temporary Files

Remove old temporary files from server.

**`DELETE /api/cleanup`**

#### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `max_age_hours` | Integer | `24` | Delete files older than this |

#### Request Example

```bash
curl -X DELETE "http://localhost:8000/api/cleanup?max_age_hours=12"
```

#### Response

```json
{
  "uploads_deleted": 5,
  "outputs_deleted": 8,
  "total_deleted": 13,
  "space_freed_mb": 156.4
}
```

---

## 🎨 Style Reference

### Image Processing Styles (Fast)

<table>
<tr>
<th>Style ID</th>
<th>Name</th>
<th>Processing Time</th>
<th>Best For</th>
</tr>
<tr>
<td><code>ultra</code></td>
<td>💎 Ultra Quality</td>
<td>10-30s</td>
<td>Best overall results, professional use</td>
</tr>
<tr>
<td><code>classic</code></td>
<td>🎨 Classic Cartoon</td>
<td>2-5s</td>
<td>General photos, portraits, landscapes</td>
</tr>
<tr>
<td><code>smooth</code></td>
<td>✨ Smooth Cartoon</td>
<td>3-7s</td>
<td>Photos with lots of detail</td>
</tr>
<tr>
<td><code>edge_heavy</code></td>
<td>🖊️ Bold Edges</td>
<td>2-5s</td>
<td>Comic book style, architecture</td>
</tr>
<tr>
<td><code>pencil_sketch</code></td>
<td>✏️ Pencil Sketch</td>
<td>2-4s</td>
<td>Black & white artistic portraits</td>
</tr>
<tr>
<td><code>pencil_sketch_color</code></td>
<td>🖍️ Colored Pencil</td>
<td>2-4s</td>
<td>Color sketch artwork</td>
</tr>
<tr>
<td><code>oil_painting</code></td>
<td>🖼️ Oil Painting</td>
<td>3-6s</td>
<td>Painterly effect, landscapes</td>
</tr>
</table>

### AI Styles (Requires PyTorch)

<table>
<tr>
<th>Style ID</th>
<th>Name</th>
<th>Processing Time</th>
<th>Best For</th>
</tr>
<tr>
<td><code>cartoon</code></td>
<td>🤖 AI Cartoon</td>
<td>5-15s</td>
<td>AI-enhanced cartoon effect</td>
</tr>
<tr>
<td><code>anime</code></td>
<td>🎌 Anime Style</td>
<td>5-20s</td>
<td>Japanese animation, character art</td>
</tr>
<tr>
<td><code>watercolor</code></td>
<td>💧 Watercolor</td>
<td>5-15s</td>
<td>Soft, artistic painting effect</td>
</tr>
</table>

> **Note:** AI styles require PyTorch installation. If not available, they fall back to OpenCV implementations.

---

## 🔧 Python Client Library

Complete Python client for easy integration:

```python
import requests
from pathlib import Path
from typing import List, Dict, Optional

class CartoonConverterClient:
    """Client for Image to Cartoon Converter API"""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url.rstrip('/')
    
    def health_check(self) -> Dict:
        """Check API health"""
        response = requests.get(f"{self.base_url}/health")
        response.raise_for_status()
        return response.json()
    
    def get_styles(self) -> Dict:
        """Get available styles"""
        response = requests.get(f"{self.base_url}/api/styles")
        response.raise_for_status()
        return response.json()
    
    def convert_image(
        self,
        image_path: str,
        style: str = "ultra",
        output_path: Optional[str] = None,
        resize_output: bool = True
    ) -> str:
        """
        Convert an image to cartoon style
        
        Args:
            image_path: Path to input image
            style: Conversion style
            output_path: Path to save output (auto-generated if None)
            resize_output: Auto-resize large images
            
        Returns:
            Path to saved cartoon image
        """
        with open(image_path, 'rb') as f:
            files = {'file': f}
            data = {
                'style': style,
                'resize_output': str(resize_output).lower()
            }
            
            response = requests.post(
                f"{self.base_url}/api/convert",
                files=files,
                data=data
            )
        
        response.raise_for_status()
        
        if output_path is None:
            output_path = f"cartoon_{style}_{Path(image_path).name}"
        
        with open(output_path, 'wb') as f:
            f.write(response.content)
        
        return output_path
    
    def batch_convert(
        self,
        image_paths: List[str],
        style: str = "ultra"
    ) -> Dict:
        """
        Convert multiple images
        
        Args:
            image_paths: List of image paths
            style: Style to apply to all images
            
        Returns:
            Batch conversion results
        """
        files = [
            ('files', open(path, 'rb'))
            for path in image_paths
        ]
        
        try:
            response = requests.post(
                f"{self.base_url}/api/batch-convert",
                files=files,
                data={'style': style}
            )
            response.raise_for_status()
            return response.json()
        finally:
            for _, f in files:
                f.close()
    
    def get_stats(self) -> Dict:
        """Get API statistics"""
        response = requests.get(f"{self.base_url}/api/stats")
        response.raise_for_status()
        return response.json()
    
    def cleanup(self, max_age_hours: int = 24) -> Dict:
        """Clean up old temporary files"""
        response = requests.delete(
            f"{self.base_url}/api/cleanup",
            params={'max_age_hours': max_age_hours}
        )
        response.raise_for_status()
        return response.json()


# Usage Example
if __name__ == "__main__":
    client = CartoonConverterClient()
    
    # Health check
    print("API Status:", client.health_check())
    
    # Get styles
    styles = client.get_styles()
    print("Available styles:", styles['classic_styles'])
    
    # Convert single image
    output = client.convert_image("photo.jpg", style="ultra")
    print(f"Saved to: {output}")
    
    # Batch convert
    results = client.batch_convert(
        ["photo1.jpg", "photo2.jpg", "photo3.jpg"],
        style="classic"
    )
    print(f"Batch results: {results['successful']}/{results['total']} succeeded")
    
    # Get statistics
    stats = client.get_stats()
    print(f"Total conversions: {stats['outputs']}")
```

---

## 🌐 JavaScript Client Library

Browser and Node.js compatible client:

```javascript
class CartoonConverterClient {
  constructor(baseUrl = 'http://localhost:8000') {
    this.baseUrl = baseUrl.replace(/\/$/, '');
  }

  async healthCheck() {
    const response = await fetch(`${this.baseUrl}/health`);
    if (!response.ok) throw new Error('Health check failed');
    return await response.json();
  }

  async getStyles() {
    const response = await fetch(`${this.baseUrl}/api/styles`);
    if (!response.ok) throw new Error('Failed to get styles');
    return await response.json();
  }

  async convertImage(file, style = 'ultra', resizeOutput = true) {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('style', style);
    formData.append('resize_output', resizeOutput.toString());

    const response = await fetch(`${this.baseUrl}/api/convert`, {
      method: 'POST',
      body: formData
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'Conversion failed');
    }

    return await response.blob();
  }

  async batchConvert(files, style = 'ultra') {
    const formData = new FormData();
    files.forEach(file => formData.append('files', file));
    formData.append('style', style);

    const response = await fetch(`${this.baseUrl}/api/batch-convert`, {
      method: 'POST',
      body: formData
    });

    if (!response.ok) throw new Error('Batch conversion failed');
    return await response.json();
  }

  async getStats() {
    const response = await fetch(`${this.baseUrl}/api/stats`);
    if (!response.ok) throw new Error('Failed to get stats');
    return await response.json();
  }

  async cleanup(maxAgeHours = 24) {
    const response = await fetch(
      `${this.baseUrl}/api/cleanup?max_age_hours=${maxAgeHours}`,
      { method: 'DELETE' }
    );
    if (!response.ok) throw new Error('Cleanup failed');
    return await response.json();
  }
}

// Usage Example
const client = new CartoonConverterClient();

// Get available styles
const styles = await client.getStyles();
console.log('Available:', styles.classic_styles);

// Convert image
const fileInput = document.querySelector('input[type="file"]');
const blob = await client.convertImage(fileInput.files[0], 'ultra');
const imageUrl = URL.createObjectURL(blob);

// Display result
const img = document.createElement('img');
img.src = imageUrl;
document.body.appendChild(img);
```

---

## 📊 Response Time Reference

| Operation | Typical Time |
|-----------|--------------|
| Health Check | < 10ms |
| Get Styles | < 50ms |
| Convert (Ultra Quality) | 10-30s |
| Convert (Classic Styles) | 2-7s |
| Convert (AI Styles) | 5-20s |
| Batch Convert (3 images) | 15-60s |
| Cleanup | < 500ms |

---

## 🔒 Security Notes

- No authentication required (suitable for local/development use)
- For production: Add API keys, rate limiting, and HTTPS
- File uploads are validated for type and size
- Temporary files auto-cleaned after 24 hours
- CORS enabled for frontend integration

---

## 📚 Additional Resources

- **Main Documentation:** [README.md](README.md)
- **Quick Start Guide:** [QUICKSTART.md](QUICKSTART.md)
- **Development Guide:** [DEVELOPMENT.md](DEVELOPMENT.md)
- **Testing Examples:** [examples/README.md](examples/README.md)

---

<div align="center">

**Need help?** Check the [Quick Start troubleshooting](QUICKSTART.md#-troubleshooting) or [open an issue](https://github.com/rogerdemello/ImageToToonArt/issues)

</div>
