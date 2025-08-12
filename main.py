import os
import json
import logging
from typing import List

# ✅ Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Configuration
OUTPUT_DIR = os.path.join(os.getcwd(), "output")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Dynamically import parsers based on extension
def get_parser(ext: str):
    if ext == '.xml':
        from xml_parser import XMLParser
        return XMLParser()
    elif ext == '.txt':
        from txt_parser import TXTParser
        return TXTParser()
    elif ext in ['.ppt', '.pptx']:
        from ppt_parser import PPTParser
        return PPTParser()
    else:
        raise ValueError(f"Unsupported file extension: {ext}")

def parse_and_save(file_path: str, uploaded_by: str = "") -> None:
    ext = os.path.splitext(file_path)[1].lower()
    try:
        parser = get_parser(ext)
        parsed_data = parser.parse_file(file_path, uploaded_by)
        
        base_name = os.path.splitext(os.path.basename(file_path))[0]
        output_filename = f"{base_name}_parsed.json"
        output_path = os.path.join(OUTPUT_DIR, output_filename)
        
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(parsed_data, f, indent=2)
        
        logging.info(f"✅ Parsed data saved to: {output_path}")
    except Exception as e:
        logging.error(f"❌ Error processing {file_path}: {e}")

def process_multiple_files(file_paths: List[str], uploaded_by: str = "") -> None:
    for file_path in file_paths:
        parse_and_save(file_path, uploaded_by)

if __name__ == "__main__":
    # Example: Process multiple files
    input_files = [
        "uploads/clinical_notes.txt",
        "uploads/pub.xml",
        "uploads/hello.pptx",
    ]
    process_multiple_files(input_files, "jane@example.com")
    
    # Or for single file: parse_and_save("uploads/sample.html")
