# Docker Usage Guide

## Build the Docker Image

```bash
docker build -t pdf-extractor .
```

## Run the Container

### Basic Usage (for hackathon submission)
Place PDF files in an `input` directory and run:

```bash
# Create input directory
mkdir input

# Place your PDF files in the input directory
# cp your_file.pdf input/

# Run the container with volume mounts
docker run --rm -v "$(pwd)/input:/app/input" -v "$(pwd)/output:/app/output" pdf-extractor
```

### Alternative Usage (with data directory)
```bash
# Create data directory
mkdir data

# Place your PDF files in the data directory
# cp your_file.pdf data/

# Run the container
docker run --rm -v "$(pwd)/data:/app/data" pdf-extractor
```

## Expected Output

The application will:
1. Process all PDF files found in the input directory
2. Extract structured outlines (Title, H1, H2, H3) from each PDF
3. Save results as JSON files in the output directory
4. Each JSON file will contain:
   - `title`: The document title
   - `outline`: Array of headings with level, text, and page number

## Example Output Structure

```json
{
  "title": "Document Title",
  "outline": [
    {
      "level": "H1",
      "text": "Introduction",
      "page": 1
    },
    {
      "level": "H2", 
      "text": "Overview",
      "page": 2
    }
  ]
}
```

## Troubleshooting

1. **No PDF files found**: Ensure PDF files are in the correct input directory
2. **Permission errors**: Make sure the mounted directories have proper permissions
3. **Memory issues**: For large PDFs, ensure Docker has sufficient memory allocated

## Container Specifications

- **Base Image**: python:3.9-slim
- **Architecture**: Compatible with AMD64
- **Dependencies**: PyMuPDF, pypdf, pdfplumber, pypdfium2
- **Processing Time**: ≤ 10 seconds for 50-page PDF
- **Resource Requirements**: CPU only, no GPU required
