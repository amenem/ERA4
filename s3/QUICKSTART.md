# 🚀 Quick Start Guide

Get your ERA4 Frontend application running in 3 simple steps!

**Note**: This project is located in the `s3/` subdirectory of the ERA4 repository.

## Prerequisites
- Python 3.8.1 or higher
- UV package manager (recommended)

## Step 1: Navigate to Project Directory
```bash
cd s3/
```

## Step 2: Install Dependencies
```bash
uv sync
```

## Step 3: Download Animal Images
```bash
uv run python setup_images.py
```

## Step 4: Run the Application
```bash
uv run python main.py
```

## 🎯 That's it!

- **Frontend**: http://localhost:8001
- **API Docs**: http://localhost:8001/docs

## ✨ Features Ready to Use

1. **Animal Selector**: Choose cat, dog, or elephant to see beautiful images
2. **File Upload**: Drag & drop or click to upload any file
3. **File Info**: Get detailed file metadata (name, size, type)

## 🛠️ Alternative Commands

- **Using run.py**: `uv run python run.py`
- **Development mode**: `uv run uvicorn main:app --reload --host 0.0.0.0 --port 8001`

## 🆘 Need Help?

- Check the full [README.md](../README.md) for detailed instructions
- Ensure port 8001 is available (change port in main.py if needed)
- Verify all dependencies are installed with `uv sync`

## 📁 Project Location

This project is now organized in the `s3/` subdirectory:
```
ERA4/
├── s3/                  # ← You are here
│   ├── main.py          # FastAPI application
│   ├── static/images/   # Animal images
│   └── ...              # Other project files
└── README.md            # Main documentation
```

Happy coding! 🎉 