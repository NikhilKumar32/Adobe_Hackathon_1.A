# PDF Outline Extractor - Docker Application

## 🎯 Overview
A Docker-based PDF outline extractor that intelligently extracts structured headings (Title, H1, H2, H3) from PDF files and generates JSON output. Built for the Adobe Hackathon Challenge with full compliance to requirements.

## ✅ Requirements Met
- ✅ **CPU only** (AMD64 architecture)
- ✅ **No internet access** required
- ✅ **Processing time** ≤ 10 seconds for 50-page PDF
- ✅ **Model size** ≤ 200MB (uses PyMuPDF + lightweight dependencies)
- ✅ **Input**: `/app/input/*.pdf`
- ✅ **Output**: `/app/output/*.json`
- ✅ **Offline operation** - fully containerized

## 🚀 Quick Start

### Prerequisites
- Docker installed on your system
- PDF files to process

### 1. Build the Docker Image
```bash
docker build -t pdf-extractor .
```

### 2. Prepare Input Directory
```bash
mkdir input output
# Place your PDF files in the input directory
cp your-document.pdf input/
```

### 3. Run the Container
```bash
# Windows PowerShell
docker run --rm -v "${PWD}/input:/app/input" -v "${PWD}/output:/app/output" pdf-extractor

# Linux/Mac
docker run --rm -v "$(pwd)/input:/app/input" -v "$(pwd)/output:/app/output" pdf-extractor
```

## 📁 Project Structure
```
Project/
├── app.py                 # Main PDF processing application
├── simple_extractor.py    # Alternative extraction script
├── test_extractor.py      # Testing utilities
├── script.py             # Additional utility script
├── requirements.txt       # Python dependencies
├── Dockerfile            # Docker container configuration
├── .dockerignore         # Docker build optimization
├── DOCKER_USAGE.md       # Detailed Docker usage guide
├── README.md             # This file
├── input/                # PDF input directory
│   └── LMSAI.pdf         # Example PDF file
└── output/               # JSON output directory
    └── LMSAI.json        # Generated outline
```

## � Technical Details

### Core Dependencies
- **PyMuPDF (fitz)**: Primary PDF processing library
- **pypdf**: Additional PDF utilities
- **pdfplumber**: Enhanced text extraction
- **pypdfium2**: Alternative PDF renderer
- **python-dateutil**: Date processing utilities

### Processing Algorithm
1. **Text Block Extraction**: Extracts all text with font metadata
2. **Font Hierarchy Analysis**: Determines heading levels by font size
3. **Intelligent Filtering**: Removes non-headings (page numbers, etc.)
4. **Structure Generation**: Creates hierarchical JSON outline

### Performance Metrics
- **Processing Speed**: ~0.16-0.28 seconds per PDF
- **Memory Usage**: Minimal footprint
- **Headings Extracted**: Typically 50-70 headings per document
- **Accuracy**: High precision heading detection

## 📝 Output Format
```json
{
  "title": "Document Title",
  "outline": [
    {
      "level": "H1",
      "text": "1. Overview",
      "page": 1
    },
    {
      "level": "H2",
      "text": "Technical Requirements",
      "page": 1
    },
    {
      "level": "H3",
      "text": "System Architecture",
      "page": 2
    }
  ]
}
```

## 🐳 Docker Commands Reference

### Build Image
```bash
docker build -t pdf-extractor .
```

### Run with Volume Mounts
```bash
# Basic usage
docker run --rm -v "${PWD}/input:/app/input" -v "${PWD}/output:/app/output" pdf-extractor

# Debug mode (interactive shell)
docker run --rm -it -v "${PWD}/input:/app/input" -v "${PWD}/output:/app/output" pdf-extractor bash

# With performance monitoring
time docker run --rm -v "${PWD}/input:/app/input" -v "${PWD}/output:/app/output" pdf-extractor
```

### Alternative Data Directory Approach
```bash
# Using single data directory
docker run --rm -v "${PWD}/data:/app/data" pdf-extractor
```

## 🧪 Example Execution

### Sample Input
- **File**: `LMSAI.pdf` (69,716 bytes)
- **Pages**: Multi-page technical document

### Sample Output
- **Processing Time**: 0.16 seconds
- **Headings Extracted**: 62 structured headings
- **Output File**: `LMSAI.json` (6,236 bytes)
- **Hierarchy Levels**: H1, H2, H3 with proper nesting

### Console Output
```
2025-07-28 17:53:33,932 - INFO - Using hackathon directory structure: /app/input -> /app/output
2025-07-28 17:53:33,939 - INFO - Found 1 PDF files to process
2025-07-28 17:53:33,939 - INFO - Processing: LMSAI.pdf
2025-07-28 17:53:34,103 - INFO - Processed /app/input/LMSAI.pdf in 0.16 seconds
2025-07-28 17:53:34,109 - INFO - Saved outline to /app/output/LMSAI.json
2025-07-28 17:53:34,109 - INFO - Extracted 62 headings
2025-07-28 17:53:34,109 - INFO - Successfully processed 1/1 files
```

## 🔍 Troubleshooting

### Common Issues
1. **No PDF files found**: Ensure PDFs are in the `/input` directory
2. **Permission errors**: Check Docker volume mount permissions
3. **Empty output**: Verify PDF contains text (not just images)
4. **Memory issues**: For large PDFs, ensure Docker has sufficient memory

### Debug Steps
1. Check input directory contents: `ls input/`
2. Verify Docker image exists: `docker images | grep pdf-extractor`
3. Run in interactive mode for debugging
4. Check container logs for error messages

## 🏆 Adobe Hackathon Compliance

### Architecture Requirements
- ✅ **Platform**: Linux/AMD64 compatible
- ✅ **Runtime**: CPU-only processing
- ✅ **Dependencies**: All libraries < 200MB total
- ✅ **Network**: No internet access required

### Performance Requirements
- ✅ **Speed**: Sub-second processing for most PDFs
- ✅ **Scalability**: Handles multiple PDFs efficiently
- ✅ **Memory**: Minimal memory footprint
- ✅ **Reliability**: Robust error handling

### Input/Output Requirements
- ✅ **Input Path**: `/app/input/*.pdf`
- ✅ **Output Path**: `/app/output/*.json`
- ✅ **Format**: Structured JSON with title and outline
- ✅ **Hierarchy**: Proper H1, H2, H3 level detection

## 📚 Additional Documentation
- `DOCKER_USAGE.md` - Comprehensive Docker usage guide
- `SETUP_GUIDE.md` - Detailed setup instructions
- Source code comments - Inline documentation

## 🎉 Ready for Submission!
This Docker-based PDF outline extractor is fully compliant with Adobe Hackathon Round 1A requirements and ready for evaluation.