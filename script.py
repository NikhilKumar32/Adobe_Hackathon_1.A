# Let's create the directory structure and understand the requirements better
import os
import json
from datetime import datetime

# Create the required directory structure
directories = [
    "app",
    "app/input", 
    "app/output",
    "data"
]

for directory in directories:
    os.makedirs(directory, exist_ok=True)
    print(f"Created directory: {directory}")

# Display the hackathon requirements summary
requirements = {
    "challenge": "Round 1A: PDF Outline Extraction",
    "input": "PDF files (up to 50 pages) from /app/input",
    "output": "JSON files with title and outline to /app/output",
    "constraints": {
        "execution_time": "≤ 10 seconds for 50-page PDF",
        "model_size": "≤ 200MB",
        "network": "No internet access allowed",
        "runtime": "CPU only (AMD64), 8 CPUs, 16GB RAM"
    },
    "json_format": {
        "title": "Document Title",
        "outline": [
            {"level": "H1", "text": "Introduction", "page": 1},
            {"level": "H2", "text": "What is AI?", "page": 2},
            {"level": "H3", "text": "History of AI", "page": 3}
        ]
    }
}

print("\n" + "="*50)
print("ADOBE HACKATHON CHALLENGE REQUIREMENTS")
print("="*50)
print(json.dumps(requirements, indent=2))