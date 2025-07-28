#!/usr/bin/env python3
"""
Test Script for PDF Outline Extractor
=====================================

This script tests the PDF outline extraction functionality
and validates the output format.
"""

import os
import json
import sys
import time
from simple_extractor import extract_pdf_outline

def create_test_structure():
    """Create test directory structure."""
    directories = ["data", "app/input", "app/output", "test_samples"]
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"✅ Created directory: {directory}")

def validate_json_output(json_data):
    """Validate JSON output format."""
    required_keys = ["title", "outline"]
    
    # Check required keys
    for key in required_keys:
        if key not in json_data:
            return False, f"Missing required key: {key}"
    
    # Check title
    if not isinstance(json_data["title"], str):
        return False, "Title must be a string"
    
    # Check outline
    if not isinstance(json_data["outline"], list):
        return False, "Outline must be a list"
    
    # Check outline items
    for item in json_data["outline"]:
        if not isinstance(item, dict):
            return False, "Outline items must be dictionaries"
        
        required_item_keys = ["level", "text", "page"]
        for key in required_item_keys:
            if key not in item:
                return False, f"Missing key in outline item: {key}"
        
        # Check level
        if item["level"] not in ["H1", "H2", "H3"]:
            return False, f"Invalid level: {item['level']}"
        
        # Check text
        if not isinstance(item["text"], str) or len(item["text"]) == 0:
            return False, "Text must be a non-empty string"
        
        # Check page
        if not isinstance(item["page"], int) or item["page"] < 1:
            return False, "Page must be a positive integer"
    
    return True, "JSON format is valid"

def test_pdf_processing():
    """Test PDF processing functionality."""
    print("\n" + "="*50)
    print("PDF OUTLINE EXTRACTOR TEST")
    print("="*50)
    
    # Create test structure
    create_test_structure()
    
    # Look for test PDFs
    test_locations = ["data", "test_samples", "app/input"]
    test_pdfs = []
    
    for location in test_locations:
        if os.path.exists(location):
            pdfs = [f for f in os.listdir(location) if f.lower().endswith('.pdf')]
            for pdf in pdfs:
                test_pdfs.append(os.path.join(location, pdf))
    
    if not test_pdfs:
        print("⚠️  No test PDFs found. Please add PDF files to one of these directories:")
        for location in test_locations:
            print(f"   - {location}/")
        return False
    
    print(f"📄 Found {len(test_pdfs)} test PDF(s)")
    
    # Process each PDF
    success_count = 0
    for pdf_path in test_pdfs:
        print(f"\n📖 Processing: {os.path.basename(pdf_path)}")
        
        try:
            # Time the processing
            start_time = time.time()
            outline = extract_pdf_outline(pdf_path)
            processing_time = time.time() - start_time
            
            # Validate output
            is_valid, message = validate_json_output(outline)
            
            if is_valid:
                print(f"✅ Processing successful in {processing_time:.2f} seconds")
                print(f"📊 Title: {outline['title']}")
                print(f"📊 Headings found: {len(outline['outline'])}")
                
                # Show heading breakdown
                heading_counts = {"H1": 0, "H2": 0, "H3": 0}
                for item in outline['outline']:
                    heading_counts[item['level']] += 1
                
                print(f"📊 Breakdown - H1: {heading_counts['H1']}, H2: {heading_counts['H2']}, H3: {heading_counts['H3']}")
                
                # Check performance requirement
                if processing_time <= 10:
                    print("⚡ Performance: PASSED (≤ 10 seconds)")
                else:
                    print("⚠️  Performance: WARNING (> 10 seconds)")
                
                success_count += 1
                
                # Save test output
                output_path = os.path.join("data", os.path.splitext(os.path.basename(pdf_path))[0] + "_test.json")
                with open(output_path, 'w', encoding='utf-8') as f:
                    json.dump(outline, f, indent=2, ensure_ascii=False)
                print(f"💾 Test output saved to: {output_path}")
                
            else:
                print(f"❌ Validation failed: {message}")
                
        except Exception as e:
            print(f"❌ Error processing {pdf_path}: {str(e)}")
    
    print(f"\n{'='*50}")
    print(f"TEST RESULTS: {success_count}/{len(test_pdfs)} PDFs processed successfully")
    print(f"{'='*50}")
    
    return success_count == len(test_pdfs)

def create_sample_json():
    """Create a sample JSON output for reference."""
    sample_output = {
        "title": "Understanding Artificial Intelligence",
        "outline": [
            {
                "level": "H1",
                "text": "Introduction to AI",
                "page": 1
            },
            {
                "level": "H2",
                "text": "What is Artificial Intelligence?",
                "page": 2
            },
            {
                "level": "H3",
                "text": "History of AI Development",
                "page": 3
            },
            {
                "level": "H2",
                "text": "Types of AI Systems",
                "page": 5
            },
            {
                "level": "H3",
                "text": "Machine Learning",
                "page": 6
            },
            {
                "level": "H3",
                "text": "Deep Learning",
                "page": 8
            },
            {
                "level": "H1",
                "text": "Applications of AI",
                "page": 10
            }
        ]
    }
    
    # Save sample
    with open("data/sample_output.json", 'w', encoding='utf-8') as f:
        json.dump(sample_output, f, indent=2, ensure_ascii=False)
    
    print("📄 Sample JSON output created: data/sample_output.json")

def main():
    """Main test function."""
    print("🧪 Starting PDF Outline Extractor Tests...")
    
    # Create sample JSON for reference
    create_sample_json()
    
    # Run tests
    success = test_pdf_processing()
    
    if success:
        print("\n🎉 All tests passed! Solution is ready for hackathon submission.")
    else:
        print("\n⚠️  Some tests failed. Please check the issues above.")
    
    print("\n📝 To add test PDFs:")
    print("   1. Place PDF files in the 'data/' folder")
    print("   2. Run: python test_extractor.py")
    print("   3. Check generated JSON files in 'data/'")

if __name__ == "__main__":
    main()