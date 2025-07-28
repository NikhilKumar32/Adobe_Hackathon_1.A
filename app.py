#!/usr/bin/env python3
"""
Adobe Hackathon Challenge - Round 1A: PDF Outline Extractor
============================================================

This script extracts structured outlines (Title, H1, H2, H3) from PDF files
and outputs them as JSON files with title and outline containing level, text, and page number.

Requirements:
- CPU only (AMD64)
- No internet/network calls
- Process time ≤ 10 seconds for 50-page PDF
- Model size ≤ 200MB
- Input: /app/input/*.pdf
- Output: /app/output/*.json

Author: Adobe Hackathon Participant
Date: July 17, 2025
"""

import os
import json
import fitz  # PyMuPDF
import re
import time
from typing import Dict, List, Tuple, Optional
from collections import defaultdict
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class PDFOutlineExtractor:
    """
    Intelligent PDF outline extractor that detects document structure
    based on font sizes, positioning, and formatting patterns.
    """
    
    def __init__(self):
        self.min_font_size = 8
        self.max_font_size = 72
        self.min_heading_length = 3
        self.max_heading_length = 200
        
    def extract_text_blocks(self, pdf_path: str) -> List[Dict]:
        """Extract text blocks with font information from PDF."""
        try:
            doc = fitz.open(pdf_path)
            text_blocks = []
            
            for page_num in range(len(doc)):
                page = doc[page_num]
                blocks = page.get_text("dict")["blocks"]
                
                for block in blocks:
                    if block.get("type") == 0:  # text block
                        for line in block["lines"]:
                            for span in line["spans"]:
                                text = span["text"].strip()
                                if text and len(text) >= self.min_heading_length:
                                    text_blocks.append({
                                        "text": text,
                                        "font_size": span["size"],
                                        "font_name": span["font"],
                                        "flags": span["flags"],
                                        "page": page_num + 1,
                                        "bbox": span["bbox"]
                                    })
            
            doc.close()
            return text_blocks
            
        except Exception as e:
            logger.error(f"Error extracting text from {pdf_path}: {str(e)}")
            return []
    
    def analyze_font_hierarchy(self, text_blocks: List[Dict]) -> Dict:
        """Analyze font sizes to determine heading hierarchy."""
        font_sizes = [block["font_size"] for block in text_blocks]
        font_size_counts = defaultdict(int)
        
        for size in font_sizes:
            font_size_counts[size] += 1
        
        # Sort font sizes by frequency (descending) and size (descending)
        sorted_sizes = sorted(font_size_counts.keys(), 
                            key=lambda x: (-font_size_counts[x], -x))
        
        # Identify potential heading sizes
        unique_sizes = sorted(set(font_sizes), reverse=True)
        
        hierarchy = {}
        if len(unique_sizes) >= 1:
            hierarchy["title"] = unique_sizes[0]
        if len(unique_sizes) >= 2:
            hierarchy["H1"] = unique_sizes[1]
        if len(unique_sizes) >= 3:
            hierarchy["H2"] = unique_sizes[2]
        if len(unique_sizes) >= 4:
            hierarchy["H3"] = unique_sizes[3]
        
        return hierarchy
    
    def is_potential_heading(self, text: str, font_size: float, flags: int) -> bool:
        """Determine if text is likely a heading based on various criteria."""
        # Check length constraints
        if len(text) < self.min_heading_length or len(text) > self.max_heading_length:
            return False
        
        # Check if text contains mostly numbers or special characters
        if re.match(r'^[\d\s\.\-\(\)]+$', text):
            return False
        
        # Check for common non-heading patterns
        non_heading_patterns = [
            r'^\d+\.\d+',  # Version numbers
            r'^Page \d+',  # Page numbers
            r'^Figure \d+',  # Figure captions
            r'^Table \d+',  # Table captions
            r'^www\.',  # URLs
            r'^https?://',  # URLs
            r'^\w+@\w+',  # Email addresses
        ]
        
        for pattern in non_heading_patterns:
            if re.match(pattern, text, re.IGNORECASE):
                return False
        
        # Check if text ends with common heading patterns
        heading_endings = ['.', ':', '?', '!']
        if not any(text.endswith(ending) for ending in heading_endings):
            # Most headings end with punctuation or are standalone
            if not text.isupper() and not text.istitle():
                return False
        
        return True
    
    def extract_title(self, text_blocks: List[Dict], font_hierarchy: Dict) -> str:
        """Extract document title from text blocks."""
        if not text_blocks or "title" not in font_hierarchy:
            return ""
        
        title_size = font_hierarchy["title"]
        
        # Find first text block with title font size
        for block in text_blocks:
            if (block["font_size"] == title_size and 
                block["page"] == 1 and 
                self.is_potential_heading(block["text"], block["font_size"], block["flags"])):
                return block["text"]
        
        return ""
    
    def extract_headings(self, text_blocks: List[Dict], font_hierarchy: Dict) -> List[Dict]:
        """Extract headings based on font hierarchy."""
        headings = []
        
        for block in text_blocks:
            font_size = block["font_size"]
            text = block["text"]
            
            # Skip if not a potential heading
            if not self.is_potential_heading(text, font_size, block["flags"]):
                continue
            
            # Determine heading level
            level = None
            if font_size == font_hierarchy.get("H1"):
                level = "H1"
            elif font_size == font_hierarchy.get("H2"):
                level = "H2"
            elif font_size == font_hierarchy.get("H3"):
                level = "H3"
            
            if level:
                headings.append({
                    "level": level,
                    "text": text,
                    "page": block["page"]
                })
        
        return headings
    
    def extract_outline(self, pdf_path: str) -> Dict:
        """Extract structured outline from PDF."""
        start_time = time.time()
        
        try:
            # Extract text blocks
            text_blocks = self.extract_text_blocks(pdf_path)
            if not text_blocks:
                return {"title": "", "outline": []}
            
            # Analyze font hierarchy
            font_hierarchy = self.analyze_font_hierarchy(text_blocks)
            
            # Extract title
            title = self.extract_title(text_blocks, font_hierarchy)
            
            # Extract headings
            headings = self.extract_headings(text_blocks, font_hierarchy)
            
            # Remove duplicates while preserving order
            unique_headings = []
            seen = set()
            for heading in headings:
                key = (heading["level"], heading["text"], heading["page"])
                if key not in seen:
                    seen.add(key)
                    unique_headings.append(heading)
            
            result = {
                "title": title if title else os.path.splitext(os.path.basename(pdf_path))[0],
                "outline": unique_headings
            }
            
            processing_time = time.time() - start_time
            logger.info(f"Processed {pdf_path} in {processing_time:.2f} seconds")
            
            return result
            
        except Exception as e:
            logger.error(f"Error processing {pdf_path}: {str(e)}")
            return {"title": "", "outline": []}

def process_pdf_file(pdf_path: str, output_dir: str) -> bool:
    """Process a single PDF file and save outline as JSON."""
    try:
        extractor = PDFOutlineExtractor()
        outline = extractor.extract_outline(pdf_path)
        
        # Generate output filename
        pdf_filename = os.path.splitext(os.path.basename(pdf_path))[0]
        output_path = os.path.join(output_dir, f"{pdf_filename}.json")
        
        # Save outline as JSON
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(outline, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Saved outline to {output_path}")
        logger.info(f"Extracted {len(outline['outline'])} headings")
        
        return True
        
    except Exception as e:
        logger.error(f"Error processing {pdf_path}: {str(e)}")
        return False

def process_directory(input_dir: str, output_dir: str) -> None:
    """Process all PDF files in input directory."""
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Find all PDF files
    pdf_files = [f for f in os.listdir(input_dir) if f.lower().endswith('.pdf')]
    
    if not pdf_files:
        logger.warning(f"No PDF files found in {input_dir}")
        return
    
    logger.info(f"Found {len(pdf_files)} PDF files to process")
    
    # Process each PDF file
    success_count = 0
    for pdf_file in pdf_files:
        pdf_path = os.path.join(input_dir, pdf_file)
        logger.info(f"Processing: {pdf_file}")
        
        if process_pdf_file(pdf_path, output_dir):
            success_count += 1
        else:
            logger.error(f"Failed to process: {pdf_file}")
    
    logger.info(f"Successfully processed {success_count}/{len(pdf_files)} files")

def main():
    """Main function for hackathon compliance."""
    # Standard hackathon paths
    INPUT_DIR = "/app/input"
    OUTPUT_DIR = "/app/output"
    
    # Alternative data directory structure
    DATA_DIR = "data"
    
    # Check which directory structure to use
    if os.path.exists(INPUT_DIR):
        input_path = INPUT_DIR
        output_path = OUTPUT_DIR
        logger.info("Using hackathon directory structure: /app/input -> /app/output")
    elif os.path.exists(DATA_DIR):
        input_path = DATA_DIR
        output_path = DATA_DIR
        logger.info("Using data directory structure: data -> data")
    else:
        # Create default structure
        input_path = INPUT_DIR
        output_path = OUTPUT_DIR
        os.makedirs(input_path, exist_ok=True)
        os.makedirs(output_path, exist_ok=True)
        logger.info("Created default directory structure")
    
    # Process PDFs
    process_directory(input_path, output_path)

if __name__ == "__main__":
    main()