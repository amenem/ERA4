#!/usr/bin/env python3
"""
Production configuration for ERA4 Frontend FastAPI application
Optimized for EC2 deployment with Amazon Linux
"""
import uvicorn
from main import app

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",  # Bind to all interfaces
        port=8001,        # Internal port (Nginx will proxy from 80)
        workers=4,        # Multiple workers for better performance
        log_level="info",
        access_log=True,
        # Production optimizations
        loop="uvloop",    # Faster event loop (Linux only)
        http="httptools", # Faster HTTP parser
        # Security settings
        server_header=False,  # Don't expose server info
        date_header=True,
        # Performance settings
        limit_concurrency=1000,
        limit_max_requests=10000,
        timeout_keep_alive=30,
        timeout_graceful_shutdown=30
    ) 