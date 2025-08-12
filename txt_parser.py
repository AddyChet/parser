import chardet
import os
from base_parser import BaseParser
from typing import List, Dict, Any


class TXTParser(BaseParser):
    """Parser for TXT files"""
    
    def __init__(self):
        super().__init__("txt")
    
    def extract_text_content(self, file_path: str) -> str:
        try:
            with open(file_path, 'rb') as f:
                raw_data = f.read()
                encoding = chardet.detect(raw_data)['encoding'] or 'utf-8'
            
            with open(file_path, 'r', encoding=encoding) as f:
                content = f.read()
            
            lines = (line.strip() for line in content.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            cleaned_text = ' '.join(chunk for chunk in chunks if chunk)
            
            return cleaned_text
        
        except Exception as e:
            print(f"Error extracting text from {file_path}: {e}")
            return ""
    
    def extract_sections(self, file_path: str) -> List[str]:
        try:
            with open(file_path, 'rb') as f:
                raw_data = f.read()
                encoding = chardet.detect(raw_data)['encoding'] or 'utf-8'
            
            with open(file_path, 'r', encoding=encoding) as f:
                content = f.read()
            
            # Split into paragraphs based on blank lines
            sections = [para.strip() for para in content.split('\n\n') if para.strip() and len(para) > 10]
            
            if not sections:
                full_text = self.extract_text_content(file_path)
                if full_text:
                    sections = [full_text]
            
            return sections
        
        except Exception as e:
            print(f"Error extracting sections from {file_path}: {e}")
            return [self.extract_text_content(file_path)]
    
    def parse_file(self, file_path: str, uploaded_by: str = "") -> Dict[str, Any]:
        """Parse a TXT file and return structured + unstructured format"""
        try:
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"File not found: {file_path}")
            
            # Extract sections (paragraphs)
            sections = self.extract_sections(file_path)
            
            # Generate file ID once for consistency
            file_id = self.generate_file_id()
            
            # Create structured data (each paragraph as separate post)
            structured = []
            for i, section in enumerate(sections, 1):
                section_text = f"Paragraph {i}: {section}"
                structured.append(self.create_post(file_id, section_text))
            
            # Create unstructured data (full combined text)
            full_text = " ".join(sections)
            unstructured = [self.create_post(file_id, full_text)] if full_text else []
            
            # Return in the requested format
            return {
                "structured": structured,
                "unstructured": unstructured
            }
            
        except Exception as e:
            return {
                "structured": [],
                "unstructured": [{
                    'error': str(e),
                    'file_path': file_path,
                    'source_type': self.source_type
                }]
            }
