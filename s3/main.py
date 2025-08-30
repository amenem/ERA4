from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse
import os
import aiofiles
from pathlib import Path

app = FastAPI(title="ERA4 Frontend", version="1.0.0")

# Create static directory for images and frontend files
static_dir = Path("static")
static_dir.mkdir(exist_ok=True)
images_dir = static_dir / "images"
images_dir.mkdir(exist_ok=True)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def read_root():
    """Serve the main HTML page"""
    html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ERA4 - Animal Selector & File Upload</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 30px;
            align-items: start;
        }
        
        .box {
            background: white;
            border-radius: 20px;
            padding: 30px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }
        
        .box:hover {
            transform: translateY(-5px);
            box-shadow: 0 25px 50px rgba(0,0,0,0.15);
        }
        
        .box h2 {
            color: #333;
            margin-bottom: 20px;
            text-align: center;
            font-size: 24px;
            font-weight: 600;
        }
        
        .animal-options {
            display: flex;
            flex-direction: column;
            gap: 15px;
            margin-bottom: 20px;
        }
        
        .animal-option {
            display: flex;
            align-items: center;
            gap: 12px;
            padding: 15px;
            border: 2px solid #e1e5e9;
            border-radius: 12px;
            cursor: pointer;
            transition: all 0.3s ease;
        }
        
        .animal-option:hover {
            border-color: #667eea;
            background-color: #f8f9ff;
        }
        
        .animal-option input[type="radio"] {
            width: 20px;
            height: 20px;
            accent-color: #667eea;
        }
        
        .animal-option label {
            font-size: 18px;
            font-weight: 500;
            color: #333;
            cursor: pointer;
            flex: 1;
        }
        
        .animal-image {
            width: 100%;
            max-width: 300px;
            height: 200px;
            object-fit: cover;
            border-radius: 12px;
            margin: 20px auto;
            display: block;
            box-shadow: 0 10px 20px rgba(0,0,0,0.1);
        }
        
        .file-upload-area {
            border: 3px dashed #667eea;
            border-radius: 15px;
            padding: 40px 20px;
            text-align: center;
            cursor: pointer;
            transition: all 0.3s ease;
            margin-bottom: 20px;
        }
        
        .file-upload-area:hover {
            border-color: #764ba2;
            background-color: #f8f9ff;
        }
        
        .file-upload-area.dragover {
            border-color: #764ba2;
            background-color: #f0f2ff;
            transform: scale(1.02);
        }
        
        .file-upload-area p {
            color: #667eea;
            font-size: 18px;
            font-weight: 500;
            margin-bottom: 10px;
        }
        
        .file-upload-area small {
            color: #888;
            font-size: 14px;
        }
        
        #fileInput {
            display: none;
        }
        
        .file-info {
            background: #f8f9ff;
            border-radius: 12px;
            padding: 20px;
            margin-top: 20px;
            border-left: 4px solid #667eea;
        }
        
        .file-info h3 {
            color: #333;
            margin-bottom: 15px;
            font-size: 18px;
        }
        
        .file-info p {
            color: #666;
            margin-bottom: 8px;
            font-size: 16px;
        }
        
        .file-info strong {
            color: #333;
        }
        
        .btn {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            padding: 12px 24px;
            border-radius: 8px;
            font-size: 16px;
            font-weight: 500;
            cursor: pointer;
            transition: all 0.3s ease;
            margin-top: 15px;
        }
        
        .btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 20px rgba(102, 126, 234, 0.3);
        }
        
        .btn:disabled {
            opacity: 0.6;
            cursor: not-allowed;
            transform: none;
        }
        
        .loading {
            display: none;
            text-align: center;
            margin: 20px 0;
        }
        
        .spinner {
            border: 3px solid #f3f3f3;
            border-top: 3px solid #667eea;
            border-radius: 50%;
            width: 30px;
            height: 30px;
            animation: spin 1s linear infinite;
            margin: 0 auto 10px;
        }
        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        
        @media (max-width: 768px) {
            .container {
                grid-template-columns: 1fr;
                gap: 20px;
            }
            
            .box {
                padding: 20px;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <!-- Animal Selection Box -->
        <div class="box">
            <h2>🐾 Select an Animal</h2>
            <div class="animal-options">
                <div class="animal-option">
                    <input type="radio" id="cat" name="animal" value="cat">
                    <label for="cat">🐱 Cat</label>
                </div>
                <div class="animal-option">
                    <input type="radio" id="dog" name="animal" value="dog">
                    <label for="dog">🐕 Dog</label>
                </div>
                <div class="animal-option">
                    <input type="radio" id="elephant" name="animal" value="elephant">
                    <label for="elephant">🐘 Elephant</label>
                </div>
            </div>
            <img id="animalImage" class="animal-image" style="display: none;" alt="Selected animal">
        </div>
        
        <!-- File Upload Box -->
        <div class="box">
            <h2>📁 Upload a File</h2>
            <div class="file-upload-area" id="uploadArea">
                <p>📤 Click to upload or drag & drop</p>
                <small>Any file type accepted</small>
                <input type="file" id="fileInput" accept="*/*">
            </div>
            <button class="btn" id="uploadBtn" disabled>Upload File</button>
            
            <div class="loading" id="loading">
                <div class="spinner"></div>
                <p>Uploading...</p>
            </div>
            
            <div class="file-info" id="fileInfo" style="display: none;">
                <h3>📋 File Information</h3>
                <div id="fileDetails"></div>
            </div>
        </div>
    </div>

    <script>
        // Animal selection functionality
        const animalOptions = document.querySelectorAll('input[name="animal"]');
        const animalImage = document.getElementById('animalImage');
        
        animalOptions.forEach(option => {
            option.addEventListener('change', function() {
                const selectedAnimal = this.value;
                showAnimalImage(selectedAnimal);
            });
        });
        
        function showAnimalImage(animal) {
            const imageMap = {
                'cat': '/static/images/cat.jpg',
                'dog': '/static/images/dog.jpg',
                'elephant': '/static/images/elephant.jpg'
            };
            
            animalImage.src = imageMap[animal];
            animalImage.style.display = 'block';
            animalImage.alt = `${animal.charAt(0).toUpperCase() + animal.slice(1)}`;
        }
        
        // File upload functionality
        const uploadArea = document.getElementById('uploadArea');
        const fileInput = document.getElementById('fileInput');
        const uploadBtn = document.getElementById('uploadBtn');
        const loading = document.getElementById('loading');
        const fileInfo = document.getElementById('fileInfo');
        const fileDetails = document.getElementById('fileDetails');
        
        let selectedFile = null;
        
        // Click to upload
        uploadArea.addEventListener('click', () => {
            fileInput.click();
        });
        
        // Drag and drop functionality
        uploadArea.addEventListener('dragover', (e) => {
            e.preventDefault();
            uploadArea.classList.add('dragover');
        });
        
        uploadArea.addEventListener('dragleave', () => {
            uploadArea.classList.remove('dragover');
        });
        
        uploadArea.addEventListener('drop', (e) => {
            e.preventDefault();
            uploadArea.classList.remove('dragover');
            const files = e.dataTransfer.files;
            if (files.length > 0) {
                handleFileSelection(files[0]);
            }
        });
        
        // File input change
        fileInput.addEventListener('change', (e) => {
            if (e.target.files.length > 0) {
                handleFileSelection(e.target.files[0]);
            }
        });
        
        function handleFileSelection(file) {
            selectedFile = file;
            uploadBtn.disabled = false;
            
            // Show file preview
            uploadArea.innerHTML = `
                <p>📁 Selected: ${file.name}</p>
                <small>Size: ${formatFileSize(file.size)} | Type: ${file.type || 'Unknown'}</small>
            `;
        }
        
        function formatFileSize(bytes) {
            if (bytes === 0) return '0 Bytes';
            const k = 1024;
            const sizes = ['Bytes', 'KB', 'MB', 'GB'];
            const i = Math.floor(Math.log(bytes) / Math.log(k));
            return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
        }
        
        // Upload button click
        uploadBtn.addEventListener('click', async () => {
            if (!selectedFile) return;
            
            const formData = new FormData();
            formData.append('file', selectedFile);
            
            loading.style.display = 'block';
            uploadBtn.disabled = true;
            
            try {
                const response = await fetch('/upload', {
                    method: 'POST',
                    body: formData
                });
                
                if (response.ok) {
                    const result = await response.json();
                    displayFileInfo(result);
                } else {
                    throw new Error('Upload failed');
                }
            } catch (error) {
                console.error('Upload error:', error);
                alert('Upload failed. Please try again.');
            } finally {
                loading.style.display = 'none';
                uploadBtn.disabled = false;
            }
        });
        
        function displayFileInfo(fileInfo) {
            fileDetails.innerHTML = `
                <p><strong>Name:</strong> ${fileInfo.filename}</p>
                <p><strong>Size:</strong> ${formatFileSize(fileInfo.size)}</p>
                <p><strong>Type:</strong> ${fileInfo.content_type || 'Unknown'}</p>
            `;
            fileInfo.style.display = 'block';
        }
    </script>
</body>
</html>
    """
    return HTMLResponse(content=html_content)

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    """Handle file upload and return file information"""
    try:
        # Get file information
        file_info = {
            "filename": file.filename,
            "size": 0,
            "content_type": file.content_type
        }
        
        # Read file content to get size
        content = await file.read()
        file_info["size"] = len(content)
        
        return JSONResponse(content=file_info)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"File upload failed: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001) 