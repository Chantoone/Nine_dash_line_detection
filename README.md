# Nine Dash Line Detection System

A comprehensive system for detecting the "Nine Dash Line" (also known as "đường lưỡi bò") in images, videos, and PDF documents using deep learning.

## Features

- **Multi-format Support**: Process images (JPG, PNG), videos (MP4, AVI), and documents (PDF)
- **AI-powered Detection**: Faster R-CNN model trained specifically for Nine Dash Line detection
- **Visual Results**: View detection results with highlighted bounding boxes
- **User-friendly Interface**: Easy-to-use web interface for uploading and reviewing results
- **Dashboard**: View system statistics and performance metrics

## System Architecture

- **Backend**: FastAPI application handling file uploads, AI processing, and results
- **Frontend**: React application with Tailwind CSS for a responsive user interface
- **AI Model**: Faster R-CNN with ResNet-50 backbone for detection

## Getting Started

### Prerequisites

- Python 3.8+
- Node.js 14+
- npm or yarn
- CUDA-compatible GPU (optional, for faster processing)

### Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/nine-dash-line-detection.git
   cd nine-dash-line-detection
   ```

2. Install backend dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Install frontend dependencies:
   ```
   cd frontend
   npm install
   cd ..
   ```

### Running the Application
**Backend:**
```
uvicorn app.main:app --reload
```

**Frontend:**
```
cd frontend
npm run dev
```

## Usage

1. Open your browser and navigate to http://localhost:3000
2. Use the upload interface to upload an image, video, or PDF
3. Wait for the processing to complete
4. View the detection results, including whether the Nine Dash Line was detected and visual highlights

## Project Structure

```
nine_dash_line_detection/
├── app/                     # Backend application
│   ├── api/                 # API endpoints
│   ├── core/                # Core functionality (config, model)
│   ├── services/            # Processing services for different file types
│   └── utils/               # Utility functions
├── frontend/                # React frontend
│   ├── public/              # Static assets
│   └── src/                 # React source code
├── model/                   # AI model files
├── uploads/                 # Temporary storage for uploaded files
├── results/                 # Storage for processed results
└── requirements.txt         # Python dependencies
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- This project uses the Faster R-CNN implementation from PyTorch's torchvision
- The frontend is built with React and Tailwind CSS
- File processing utilizes OpenCV, pdf2image, and Pillow
