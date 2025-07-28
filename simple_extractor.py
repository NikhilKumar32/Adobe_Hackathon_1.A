#!/usr/bin/env python3
"""
Simplified PDF Outline Extractor Backend Script
===============================================

This is a lightweight backend script that focuses purely on PDF processing
without additional frameworks or dependencies.

Usage:
    python simple_extractor.py <input_pdf_path> <output_json_path>
    or
    python simple_extractor.py (processes all PDFs in data/ folder)
"""

import os
import json
import fitz  # PyMuPDF
import re
import sys
from collections import defaultdict

def extract_pdf_outline(pdf_path):
    """
    Extract structured outline from PDF using intelligent heading detection.
    
    Args:
        pdf_path (str): Path to the PDF file
        
    Returns:
        dict: Contains title and outline with heading levels
    """
    try:
        doc = fitz.open(pdf_path)
        
        # Step 1: Extract all text with font information
        text_blocks = []
        font_sizes = []
        
        for page_num in range(len(doc)):
            page = doc[page_num]
            blocks = page.get_text("dict")["blocks"]
            
            for block in blocks:
                if block.get("type") == 0:  # text block
                    for line in block["lines"]:
                        for span in line["spans"]:
                            text = span["text"].strip()
                            if text and len(text) >= 3:
                                font_size = span["size"]
                                text_blocks.append({
                                    "text": text,
                                    "font_size": font_size,
                                    "page": page_num + 1,
                                    "flags": span["flags"]
                                })
                                font_sizes.append(font_size)
        
        doc.close()
        
        if not text_blocks:
            return {"title": "", "outline": []}
        
        # Step 2: Analyze font hierarchy
        unique_sizes = sorted(set(font_sizes), reverse=True)
        
        # Assign heading levels based on font sizes
        font_hierarchy = {}
        if len(unique_sizes) >= 1:
            font_hierarchy["title"] = unique_sizes[0]
        if len(unique_sizes) >= 2:
            font_hierarchy["H1"] = unique_sizes[1]
        if len(unique_sizes) >= 3:
            font_hierarchy["H2"] = unique_sizes[2]
        if len(unique_sizes) >= 4:
            font_hierarchy["H3"] = unique_sizes[3]
        
        # Step 3: Extract title
        title = ""
        title_size = font_hierarchy.get("title")
        if title_size:
            for block in text_blocks:
                if (block["font_size"] == title_size and 
                    block["page"] == 1 and 
                    is_valid_heading(block["text"])):
                    title = block["text"]
                    break
        
        if not title:
            title = os.path.splitext(os.path.basename(pdf_path))[0]
        
        # Step 4: Extract headings
        headings = []
        for block in text_blocks:
            font_size = block["font_size"]
            text = block["text"]
            
            if not is_valid_heading(text):
                continue
            
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
        
        # Remove duplicates
        unique_headings = []
        seen = set()
        for heading in headings:
            key = (heading["level"], heading["text"], heading["page"])
            if key not in seen:
                seen.add(key)
                unique_headings.append(heading)
        
        return {
            "title": title,
            "outline": unique_headings
        }
        
    except Exception as e:
        print(f"Error processing {pdf_path}: {str(e)}")
        return {"title": "", "outline": []}

def is_valid_heading(text):
    """Check if text is likely a valid heading."""
    # Length constraints
    if len(text) < 3 or len(text) > 200:
        return False
    
    # Skip common non-heading patterns
    non_heading_patterns = [
        r'^\d+\.\d+',  # Version numbers
        r'^Page \d+',  # Page numbers
        r'^Figure \d+',  # Figure captions
        r'^Table \d+',  # Table captions
        r'^www\.',  # URLs
        r'^https?://',  # URLs
        r'^\w+@\w+',  # Email addresses
        r'^[\d\s\.\-\(\)]+$',  # Only numbers and punctuation
    ]
    
    for pattern in non_heading_patterns:
        if re.match(pattern, text, re.IGNORECASE):
            return False
    
    return True

def process_single_pdf(input_path, output_path):
    """Process a single PDF file."""
    print(f"Processing: {input_path}")
    
    outline = extract_pdf_outline(input_path)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(outline, f, indent=2, ensure_ascii=False)
    
    print(f"Saved outline to: {output_path}")
    print(f"Extracted {len(outline['outline'])} headings")
    
    return True

def process_data_folder():
    """Process all PDFs in the data folder."""
    data_dir = "data"
    
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
        print(f"Created {data_dir} directory")
        return
    
    pdf_files = [f for f in os.listdir(data_dir) if f.lower().endswith('.pdf')]
    
    if not pdf_files:
        print(f"No PDF files found in {data_dir}")
        return
    
    print(f"Found {len(pdf_files)} PDF files in {data_dir}")
    
    for pdf_file in pdf_files:
        input_path = os.path.join(data_dir, pdf_file)
        output_file = os.path.splitext(pdf_file)[0] + '.json'
        output_path = os.path.join(data_dir, output_file)
        
        try:
            process_single_pdf(input_path, output_path)
        except Exception as e:
            print(f"Error processing {pdf_file}: {str(e)}")

def main():
    """Main function."""
    if len(sys.argv) == 3:
        # Process single file
        input_path = sys.argv[1]
        output_path = sys.argv[2]
        process_single_pdf(input_path, output_path)
    elif len(sys.argv) == 1:
        # Process data folder
        process_data_folder()
    else:
        print("Usage:")
        print("  python simple_extractor.py <input_pdf> <output_json>")
        print("  python simple_extractor.py")

if __name__ == "__main__":
    main()