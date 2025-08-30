# ERA4 - Frontend with FastAPI Backend

A modern web application built with HTML/CSS/JavaScript frontend and FastAPI backend, featuring animal selection and file upload functionality.

## 🚀 **Quick Start**

The project is now located in the `s3/` subdirectory. To get started:

```bash
cd s3/
uv sync
uv run python setup_images.py
uv run python main.py
```

Then open your browser to: http://localhost:8001

## 📁 **Project Structure**

```
ERA4/
├── s3/                  # Main project directory
│   ├── main.py          # FastAPI application
│   ├── setup_images.py  # Script to download animal images
│   ├── run.py           # Alternative startup script
│   ├── pyproject.toml   # Project configuration (UV)
│   ├── requirements.txt # Python dependencies
│   ├── static/          # Static files directory
│   │   └── images/      # Animal images
│   │       ├── cat.jpg
│   │       ├── dog.jpg
│   │       └── elephant.jpg
│   ├── .venv/           # Virtual environment
│   ├── uv.lock          # UV lock file
│   ├── .gitignore       # Git ignore file
│   └── QUICKSTART.md    # Quick start guide
├── README.md            # This file
└── .git/                # Git repository
```

## ✨ **Features**

- 🐾 **Animal Selector**: Choose from cat, dog, or elephant with beautiful image display
- 📁 **File Upload**: Drag & drop or click to upload any file type
- 📊 **File Information**: Get detailed file metadata (name, size, type)
- 🎨 **Modern UI**: Responsive design with smooth animations and gradients
- 🚀 **FastAPI Backend**: High-performance Python backend with automatic API documentation

## 📚 **Documentation**

- **Quick Start**: See [s3/QUICKSTART.md](s3/QUICKSTART.md) for immediate setup
- **Full Documentation**: All project details are in the `s3/` directory
- **API Documentation**: Available at http://localhost:8001/docs when running

## 🛠️ **Prerequisites**

- Python 3.8.1 or higher
- UV package manager (recommended)

## 🔧 **Installation & Setup**

1. **Navigate to project directory**:
   ```bash
   cd s3/
   ```

2. **Install dependencies**:
   ```bash
   uv sync
   ```

3. **Download animal images**:
   ```bash
   uv run python setup_images.py
   ```

4. **Run the application**:
   ```bash
   uv run python main.py
   ```

## 🌐 **Usage**

- **Frontend**: http://localhost:8001
- **API Documentation**: http://localhost:8001/docs

## 📝 **License**

This project is part of the ERA4 learning series.

## 🤝 **Contributing**

Feel free to submit issues and enhancement requests!
