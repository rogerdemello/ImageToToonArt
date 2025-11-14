"""
FastAPI Backend for Image to Cartoon Converter
Provides REST API endpoints for image upload and cartoon conversion
"""

from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from fastapi.responses import StreamingResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import uvicorn
import os
import io
from datetime import datetime
from typing import Optional

# Import our custom modules
from cartoon_converter import CartoonConverter
from ai_converter import AICartoonConverter
from utils import (
    allowed_file, generate_unique_filename, ensure_dir_exists,
    read_image_from_bytes, image_to_bytes, resize_image,
    validate_image, cleanup_old_files
)

# Initialize FastAPI app
app = FastAPI(
    title="Image to Cartoon Converter API",
    description="Convert images to cartoon style using AI and image processing",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize converters
cartoon_converter = CartoonConverter()
ai_converter = AICartoonConverter()

# Directories
UPLOAD_DIR = "../uploads"
OUTPUT_DIR = "../outputs"
ensure_dir_exists(UPLOAD_DIR)
ensure_dir_exists(OUTPUT_DIR)


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "🎨 Image to Cartoon Converter API",
        "version": "1.0.0",
        "status": "running",
        "endpoints": {
            "convert": "/api/convert",
            "styles": "/api/styles",
            "health": "/health"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "converters": {
            "classic": "available",
            "ai": "available"
        }
    }


@app.get("/api/styles")
async def get_available_styles():
    """Get all available conversion styles"""
    return {
        "classic_styles": cartoon_converter.get_available_styles(),
        "ai_styles": ai_converter.get_available_styles(),
        "all_styles": {
            "classic": {
                "name": "Classic Cartoon",
                "description": "Edge detection with color quantization",
                "processing_time": "fast"
            },
            "smooth": {
                "name": "Smooth Cartoon",
                "description": "Softer edges with smooth colors",
                "processing_time": "fast"
            },
            "edge_heavy": {
                "name": "Bold Edges",
                "description": "Prominent, bold edge lines",
                "processing_time": "fast"
            },
            "pencil_sketch": {
                "name": "Pencil Sketch",
                "description": "Black and white pencil drawing effect",
                "processing_time": "fast"
            },
            "pencil_sketch_color": {
                "name": "Colored Pencil",
                "description": "Colored pencil sketch effect",
                "processing_time": "fast"
            },
            "oil_painting": {
                "name": "Oil Painting",
                "description": "Oil painting artistic style",
                "processing_time": "fast"
            },
            "cartoon": {
                "name": "AI Cartoon",
                "description": "AI-enhanced cartoon effect",
                "processing_time": "medium"
            },
            "anime": {
                "name": "Anime Style",
                "description": "Japanese anime/manga style",
                "processing_time": "medium"
            },
            "watercolor": {
                "name": "Watercolor",
                "description": "Watercolor painting effect",
                "processing_time": "medium"
            }
        }
    }


@app.post("/api/convert")
async def convert_image(
    file: UploadFile = File(...),
    style: str = Form(default="classic"),
    resize_output: bool = Form(default=True)
):
    """
    Convert uploaded image to cartoon style
    
    Parameters:
    - file: Image file to convert
    - style: Conversion style (classic, smooth, edge_heavy, anime, etc.)
    - resize_output: Whether to resize large images
    
    Returns:
    - Converted image as JPEG
    """
    
    # Validate file type
    if not allowed_file(file.filename):
        raise HTTPException(
            status_code=400,
            detail="Invalid file type. Allowed: PNG, JPG, JPEG, GIF, BMP, WEBP"
        )
    
    try:
        # Read uploaded file
        contents = await file.read()
        
        # Validate image
        is_valid, error_msg = validate_image(contents, max_size_mb=10)
        if not is_valid:
            raise HTTPException(status_code=400, detail=error_msg)
        
        # Convert bytes to image array
        image = read_image_from_bytes(contents)
        
        # Resize if needed
        if resize_output:
            image = resize_image(image, max_size=(1920, 1080))
        
        # Apply cartoon conversion based on style
        if style in ['classic', 'smooth', 'edge_heavy', 'ultra']:
            # Use OpenCV-based converter
            result = cartoon_converter.convert(image, style)
            
        elif style == 'pencil_sketch':
            result = cartoon_converter.stylize_pencil_sketch(image, color=False)
            
        elif style == 'pencil_sketch_color':
            result = cartoon_converter.stylize_pencil_sketch(image, color=True)
            
        elif style == 'oil_painting':
            result = cartoon_converter.stylize_oil_painting(image)
            
        elif style in ['cartoon', 'anime', 'watercolor']:
            # Use AI-based converter
            result = ai_converter.apply_neural_style_transfer(image, style)
            
        else:
            raise HTTPException(
                status_code=400,
                detail=f"Unknown style: {style}. Use /api/styles to see available styles."
            )
        
        # Convert result to bytes
        result_bytes = image_to_bytes(result, format='JPEG')
        
        # Return as streaming response
        return StreamingResponse(
            io.BytesIO(result_bytes),
            media_type="image/jpeg",
            headers={
                "Content-Disposition": f"attachment; filename=cartoon_{file.filename}",
                "X-Processing-Style": style,
                "X-Original-Filename": file.filename
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing image: {str(e)}"
        )


@app.post("/api/batch-convert")
async def batch_convert_images(
    files: list[UploadFile] = File(...),
    style: str = Form(default="classic")
):
    """
    Convert multiple images at once
    
    Parameters:
    - files: List of image files
    - style: Conversion style to apply to all images
    
    Returns:
    - Status and information about processed images
    """
    
    if len(files) > 10:
        raise HTTPException(
            status_code=400,
            detail="Maximum 10 files allowed in batch processing"
        )
    
    results = []
    
    for file in files:
        try:
            if not allowed_file(file.filename):
                results.append({
                    "filename": file.filename,
                    "status": "error",
                    "message": "Invalid file type"
                })
                continue
            
            contents = await file.read()
            is_valid, error_msg = validate_image(contents, max_size_mb=10)
            
            if not is_valid:
                results.append({
                    "filename": file.filename,
                    "status": "error",
                    "message": error_msg
                })
                continue
            
            # Save to outputs (in production, you might want to zip these)
            unique_filename = generate_unique_filename(file.filename)
            output_path = os.path.join(OUTPUT_DIR, unique_filename)
            
            # Process image
            image = read_image_from_bytes(contents)
            
            if style in ['classic', 'smooth', 'edge_heavy']:
                result = cartoon_converter.convert(image, style)
            else:
                result = ai_converter.apply_neural_style_transfer(image, style)
            
            # Save result
            import cv2
            cv2.imwrite(output_path, result)
            
            results.append({
                "filename": file.filename,
                "output_filename": unique_filename,
                "status": "success",
                "style": style
            })
            
        except Exception as e:
            results.append({
                "filename": file.filename,
                "status": "error",
                "message": str(e)
            })
    
    return {
        "total": len(files),
        "successful": len([r for r in results if r["status"] == "success"]),
        "failed": len([r for r in results if r["status"] == "error"]),
        "results": results
    }


@app.delete("/api/cleanup")
async def cleanup_temporary_files(max_age_hours: int = 24):
    """
    Clean up old temporary files
    
    Parameters:
    - max_age_hours: Delete files older than this (default: 24 hours)
    
    Returns:
    - Number of files deleted
    """
    
    uploads_deleted = cleanup_old_files(UPLOAD_DIR, max_age_hours)
    outputs_deleted = cleanup_old_files(OUTPUT_DIR, max_age_hours)
    
    return {
        "uploads_deleted": uploads_deleted,
        "outputs_deleted": outputs_deleted,
        "total_deleted": uploads_deleted + outputs_deleted
    }


@app.get("/api/stats")
async def get_stats():
    """Get API statistics"""
    
    def count_files(directory):
        if not os.path.exists(directory):
            return 0
        return len([f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))])
    
    return {
        "uploads": count_files(UPLOAD_DIR),
        "outputs": count_files(OUTPUT_DIR),
        "available_styles": len(cartoon_converter.get_available_styles()) + len(ai_converter.get_available_styles()),
        "server_time": datetime.now().isoformat()
    }


# Error handlers
@app.exception_handler(404)
async def not_found_handler(request, exc):
    return JSONResponse(
        status_code=404,
        content={"error": "Endpoint not found", "path": str(request.url)}
    )


@app.exception_handler(500)
async def internal_error_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={"error": "Internal server error", "message": str(exc)}
    )


# Run the application
if __name__ == "__main__":
    print("🎨 Starting Image to Cartoon Converter API...")
    print("📍 Server will be available at: http://localhost:8000")
    print("📚 API documentation at: http://localhost:8000/docs")
    print("🔧 Alternative docs at: http://localhost:8000/redoc")
    
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
