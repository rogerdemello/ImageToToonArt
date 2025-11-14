import React, { useState, useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import axios from 'axios';
import './App.css';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8000';

const STYLES = {
  ultra: {
    name: 'Ultra Quality',
    description: 'Best quality - professional results',
    emoji: '💎'
  },
  classic: {
    name: 'Classic Cartoon',
    description: 'Edge detection with color quantization',
    emoji: '🎨'
  },
  smooth: {
    name: 'Smooth Cartoon',
    description: 'Softer edges with smooth colors',
    emoji: '✨'
  },
  edge_heavy: {
    name: 'Bold Edges',
    description: 'Prominent, bold edge lines',
    emoji: '🖊️'
  },
  pencil_sketch: {
    name: 'Pencil Sketch',
    description: 'Black and white pencil drawing',
    emoji: '✏️'
  },
  pencil_sketch_color: {
    name: 'Colored Pencil',
    description: 'Colored pencil sketch effect',
    emoji: '🖍️'
  },
  oil_painting: {
    name: 'Oil Painting',
    description: 'Oil painting artistic style',
    emoji: '🖼️'
  },
  cartoon: {
    name: 'AI Cartoon',
    description: 'AI-enhanced cartoon effect',
    emoji: '🤖'
  },
  anime: {
    name: 'Anime Style',
    description: 'Japanese anime/manga style',
    emoji: '🎌'
  },
  watercolor: {
    name: 'Watercolor',
    description: 'Watercolor painting effect',
    emoji: '💧'
  }
};

function App() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [previewUrl, setPreviewUrl] = useState(null);
  const [selectedStyle, setSelectedStyle] = useState('ultra');
  const [isProcessing, setIsProcessing] = useState(false);
  const [resultImage, setResultImage] = useState(null);
  const [error, setError] = useState(null);

  const onDrop = useCallback((acceptedFiles) => {
    const file = acceptedFiles[0];
    if (file) {
      setSelectedFile(file);
      setPreviewUrl(URL.createObjectURL(file));
      setResultImage(null);
      setError(null);
    }
  }, []);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'image/*': ['.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp']
    },
    maxFiles: 1,
    multiple: false
  });

  const handleConvert = async () => {
    if (!selectedFile) {
      setError('Please select an image first');
      return;
    }

    setIsProcessing(true);
    setError(null);

    try {
      const formData = new FormData();
      formData.append('file', selectedFile);
      formData.append('style', selectedStyle);
      formData.append('resize_output', 'true');

      const response = await axios.post(`${BACKEND_URL}/api/convert`, formData, {
        responseType: 'blob',
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      });

      const imageUrl = URL.createObjectURL(response.data);
      setResultImage(imageUrl);
    } catch (err) {
      console.error('Conversion error:', err);
      setError(
        err.response?.data?.detail || 
        'Failed to convert image. Please try again.'
      );
    } finally {
      setIsProcessing(false);
    }
  };

  const handleDownload = () => {
    if (resultImage) {
      const link = document.createElement('a');
      link.href = resultImage;
      link.download = `cartoon_${selectedStyle}_${Date.now()}.jpg`;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
    }
  };

  const handleReset = () => {
    setSelectedFile(null);
    setPreviewUrl(null);
    setResultImage(null);
    setError(null);
  };

  return (
    <div className="App">
      <header className="header">
        <h1>🎨 Image to Cartoon Converter</h1>
        <p>Transform your photos into stunning cartoon artwork with AI and image processing</p>
      </header>

      <div className="container">
        {/* Upload Section */}
        <div className="upload-section">
          <div 
            {...getRootProps()} 
            className={`dropzone ${isDragActive ? 'active' : ''}`}
          >
            <input {...getInputProps()} />
            <div className="dropzone-icon">📸</div>
            {isDragActive ? (
              <p className="dropzone-text">Drop the image here...</p>
            ) : (
              <>
                <p className="dropzone-text">
                  Drag & drop an image here, or click to select
                </p>
                <p className="dropzone-subtext">
                  Supports: PNG, JPG, JPEG, GIF, BMP, WEBP (Max 10MB)
                </p>
              </>
            )}
          </div>

          {previewUrl && (
            <div style={{ textAlign: 'center', marginTop: '20px' }}>
              <img 
                src={previewUrl} 
                alt="Preview" 
                className="preview-image"
                style={{ maxHeight: '300px' }}
              />
              <p style={{ marginTop: '10px', color: '#4a5568' }}>
                📁 {selectedFile.name}
              </p>
            </div>
          )}
        </div>

        {/* Style Selector */}
        <div className="style-selector">
          <h3>Choose Cartoon Style</h3>
          <div className="style-grid">
            {Object.entries(STYLES).map(([key, style]) => (
              <div
                key={key}
                className={`style-option ${selectedStyle === key ? 'selected' : ''}`}
                onClick={() => setSelectedStyle(key)}
              >
                <div className="style-name">
                  {style.emoji} {style.name}
                </div>
                <div className="style-desc">{style.description}</div>
              </div>
            ))}
          </div>
        </div>

        {/* Error Message */}
        {error && (
          <div className="error-message">
            ❌ {error}
          </div>
        )}

        {/* Convert Button */}
        <button
          className="convert-button"
          onClick={handleConvert}
          disabled={!selectedFile || isProcessing}
        >
          {isProcessing ? '🔄 Converting...' : '✨ Convert to Cartoon'}
        </button>

        {/* Loading Indicator */}
        {isProcessing && (
          <div className="loading">
            <div className="spinner"></div>
            <p>Processing your image with {STYLES[selectedStyle].name}...</p>
            <p style={{ fontSize: '0.9rem', color: '#718096' }}>
              This may take a few seconds
            </p>
          </div>
        )}

        {/* Results Section */}
        {resultImage && (
          <div className="results-section">
            <h3>✅ Conversion Complete!</h3>
            
            <div className="image-comparison">
              <div className="image-box">
                <h4>Original</h4>
                <img src={previewUrl} alt="Original" />
              </div>
              <div className="image-box">
                <h4>Cartoonized ({STYLES[selectedStyle].name})</h4>
                <img src={resultImage} alt="Cartoonized" />
              </div>
            </div>

            <button className="download-button" onClick={handleDownload}>
              📥 Download Cartoon Image
            </button>

            <button 
              className="convert-button" 
              onClick={handleReset}
              style={{ 
                background: 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)',
                marginTop: '10px'
              }}
            >
              🔄 Convert Another Image
            </button>
          </div>
        )}
      </div>

      {/* Footer */}
      <div style={{ textAlign: 'center', marginTop: '40px', color: 'white', opacity: 0.8 }}>
        <p>Made with ❤️ using React, FastAPI, OpenCV, and PyTorch</p>
      </div>
    </div>
  );
}

export default App;
