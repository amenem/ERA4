#!/usr/bin/env python3
"""
Simple startup script for the ERA4 FastAPI application
"""
import uvicorn

if __name__ == "__main__":
    print("🚀 Starting ERA4 Frontend Application...")
    print("📱 Open your browser and go to: http://localhost:8000")
    print("📚 API Documentation: http://localhost:8000/docs")
    print("⏹️  Press Ctrl+C to stop the server")
    print("-" * 50)
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8001,
        reload=True,
        log_level="info"
    ) 