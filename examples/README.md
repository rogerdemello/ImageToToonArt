# 🎨 Example Images & Testing Guide

<div align="center">

**Test the Image to Cartoon Converter with sample images and usage examples**

[Quick Test](#-quick-test) • [Sample Images](#-sample-image-sources) • [Best Practices](#-testing-best-practices) • [Style Guide](#-style-recommendations)

</div>

---

## 🚀 Quick Test

### Option 1: Use Your Own Images

✅ **Recommended image types:**
- 📸 Portrait photos
- 🏞️ Landscapes and scenery
- 🐾 Animals
- 🏛️ Architecture
- 🌸 Close-up objects

### Option 2: Download Free Stock Images

| Source | Quality | License | Best For |
|--------|---------|---------|----------|
| [Unsplash](https://unsplash.com) | High | Free | All types |
| [Pexels](https://pexels.com) | High | Free | All types |
| [Pixabay](https://pixabay.com) | Medium-High | Free | General use |
| [Lorem Picsum](https://picsum.photos) | Medium | Free | Quick testing |

---

## 📊 Style Recommendations

### Best Styles by Subject Type

<table>
<tr>
<th>Subject</th>
<th>Recommended Styles</th>
<th>Processing Time</th>
</tr>
<tr>
<td>👤 <b>Portraits</b></td>
<td>Ultra Quality, Classic, Anime, Pencil Sketch</td>
<td>2-30s</td>
</tr>
<tr>
<td>🏞️ <b>Landscapes</b></td>
<td>Ultra Quality, Watercolor, Oil Painting</td>
<td>3-30s</td>
</tr>
<tr>
<td>🐾 <b>Animals</b></td>
<td>Smooth, Classic, Anime</td>
<td>2-15s</td>
</tr>
<tr>
<td>🏛️ <b>Architecture</b></td>
<td>Bold Edges, Pencil Sketch, Classic</td>
<td>2-7s</td>
</tr>
<tr>
<td>🌸 <b>Nature/Flowers</b></td>
<td>Watercolor, Oil Painting, Smooth</td>
<td>3-15s</td>
</tr>
<tr>
<td>🍕 <b>Food</b></td>
<td>Classic, Smooth, Oil Painting</td>
<td>2-7s</td>
</tr>
<tr>
<td>⚡ <b>Action/Sports</b></td>
<td>Bold Edges, Classic</td>
<td>2-5s</td>
</tr>
</table>

---

## 🧪 Testing Best Practices

### Image Quality Guidelines

✅ **DO:**
- Use well-lit, high-resolution images
- Choose images with clear subjects
- Ensure good contrast
- Use photos with minimal blur

❌ **AVOID:**
- Very dark or overexposed images
- Extremely low resolution (< 100×100 px)
- Heavily compressed/artifacted images
- Very blurry or out-of-focus shots

### Testing Workflow

1. **Start Simple** - Try `classic` style first (fast, reliable)
2. **Compare Styles** - Test 2-3 different styles on same image
3. **Document Results** - Note which styles work best for which subjects
4. **Optimize** - Adjust image size/quality if needed

---

## 🐍 Download Test Images (Python)

```python
import requests

def download_test_image(url, filename):
    """Download a test image from URL"""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        with open(filename, 'wb') as f:
            f.write(response.content)
        print(f"✅ Downloaded: {filename}")
        return True
    except Exception as e:
        print(f"❌ Error downloading {filename}: {e}")
        return False

# Download sample images
test_images = {
    'portrait': 'https://source.unsplash.com/800x600/?portrait,face',
    'landscape': 'https://source.unsplash.com/800x600/?landscape,nature',
    'animal': 'https://source.unsplash.com/800x600/?animal,pet',
    'architecture': 'https://source.unsplash.com/800x600/?building,architecture'
}

for name, url in test_images.items():
    download_test_image(url, f'test_{name}.jpg')
```

---

## 📦 Batch Testing Script

Test all styles on a single image:

```python
import requests
import os

def test_all_styles(image_path, output_dir='results'):
    """Test all available styles on an image"""
    
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    # Get available styles
    response = requests.get('http://localhost:8000/api/styles')
    styles = response.json()
    
    all_styles = styles.get('classic_styles', []) + styles.get('ai_styles', [])
    
    print(f"Testing {len(all_styles)} styles on {image_path}...")
    
    for style in all_styles:
        print(f"  Converting with '{style}' style...", end=' ')
        
        with open(image_path, 'rb') as f:
            response = requests.post(
                'http://localhost:8000/api/convert',
                files={'file': f},
                data={'style': style}
            )
        
        if response.status_code == 200:
            output_path = os.path.join(output_dir, f'{style}_result.jpg')
            with open(output_path, 'wb') as f:
                f.write(response.content)
            print('✅')
        else:
            print(f'❌ Error: {response.status_code}')
    
    print(f"\nResults saved to '{output_dir}/' directory")

# Usage
test_all_styles('test_portrait.jpg')
```

---

## 📈 Performance Testing

Measure processing times for different styles:

```python
import requests
import time

def benchmark_styles(image_path):
    """Benchmark all styles and report processing times"""
    
    results = []
    
    response = requests.get('http://localhost:8000/api/styles')
    styles = response.json()
    all_styles = styles.get('classic_styles', []) + styles.get('ai_styles', [])
    
    for style in all_styles:
        with open(image_path, 'rb') as f:
            start_time = time.time()
            
            response = requests.post(
                'http://localhost:8000/api/convert',
                files={'file': f},
                data={'style': style}
            )
            
            elapsed = time.time() - start_time
            
            results.append({
                'style': style,
                'time': round(elapsed, 2),
                'status': response.status_code
            })
    
    # Print results table
    print("\n{:<20} {:<12} {:<10}".format("Style", "Time (s)", "Status"))
    print("-" * 42)
    for r in sorted(results, key=lambda x: x['time']):
        print("{:<20} {:<12} {:<10}".format(
            r['style'], r['time'], r['status']
        ))

# Usage
benchmark_styles('test_image.jpg')
```

---

## 📁 Suggested Directory Structure

Organize your test images:

```
examples/
├── README.md (this file)
│
├── test_images/
│   ├── portraits/
│   │   ├── person1.jpg
│   │   └── person2.jpg
│   ├── landscapes/
│   │   ├── mountain.jpg
│   │   └── ocean.jpg
│   ├── animals/
│   │   └── cat.jpg
│   └── architecture/
│       └── building.jpg
│
├── results/
│   ├── portrait_classic.jpg
│   ├── portrait_anime.jpg
│   └── ...
│
└── scripts/
    ├── download_samples.py
    ├── batch_convert.py
    └── benchmark.py
```

---

## 💡 Testing Tips

### For Best Results

1. **Image Quality Matters**
   - Higher resolution = Better results
   - Good lighting essential
   - Clear, focused subjects

2. **Style Selection**
   - Start with `ultra` or `classic`
   - Try AI styles for artistic effects
   - Use `pencil_sketch` for B&W art

3. **Performance Optimization**
   - Classic styles are faster (2-7s)
   - AI styles produce better quality but slower (5-20s)
   - Resize large images before upload

4. **Batch Processing**
   - Process similar images with same style
   - Use scripts for automation
   - Compare results side-by-side

---

## 🔍 Troubleshooting Tests

<details>
<summary><b>Image conversion fails</b></summary>

**Check:**
- File size < 10MB
- Image dimensions valid
- Supported format (PNG, JPG, etc.)
- Backend is running

**Solution:**
```bash
# Verify backend is running
curl http://localhost:8000/health

# Check file size
ls -lh test_image.jpg
```
</details>

<details>
<summary><b>Slow processing</b></summary>

**Reasons:**
- Large image size
- AI styles take longer
- System resources

**Solution:**
- Resize images to < 1920×1080
- Use classic styles for speed
- Close resource-intensive apps
</details>

---

## 📚 Additional Resources

- **API Documentation:** [API_DOCUMENTATION.md](../API_DOCUMENTATION.md)
- **Quick Start:** [QUICKSTART.md](../QUICKSTART.md)
- **Main README:** [README.md](../README.md)

---

<div align="center">

**Happy Testing! 🎨✨**

[Report Issues](https://github.com/yourusername/ImageToToonArt/issues) • [Contribute](../DEVELOPMENT.md)

</div>
│   ├── mountain.jpg
│   └── beach.jpg
└── misc/
    ├── cat.jpg
    └── building.jpg
```

## Creating Your Own Test Suite

```python
import os
from pathlib import Path

# Test all styles on a single image
def test_all_styles(image_path):
    """
    Test all available styles on one image
    (Requires backend running)
    """
    import requests
    
    styles = ['classic', 'smooth', 'edge_heavy', 'pencil_sketch', 
              'anime', 'watercolor', 'oil_painting']
    
    results_dir = Path('test_results')
    results_dir.mkdir(exist_ok=True)
    
    for style in styles:
        print(f"Testing style: {style}")
        
        with open(image_path, 'rb') as f:
            files = {'file': f}
            data = {'style': style}
            
            response = requests.post(
                'http://localhost:8000/api/convert',
                files=files,
                data=data
            )
        
        if response.status_code == 200:
            output_file = results_dir / f"{style}_{Path(image_path).name}"
            with open(output_file, 'wb') as f:
                f.write(response.content)
            print(f"  ✓ Saved: {output_file}")
        else:
            print(f"  ✗ Error: {response.json()}")

# Usage:
# test_all_styles('sample.jpg')
```

## Need Help?

If you need sample images or have questions about which images work best, check:
- Main README.md
- QUICKSTART.md
- API_DOCUMENTATION.md

Happy testing! 🎨
