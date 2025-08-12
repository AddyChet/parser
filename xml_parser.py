import chardet
import xml.etree.ElementTree as ET
from base_parser import BaseParser
from typing import List, Dict, Any
import os


class XMLParser(BaseParser):
    """Parser for XML files"""
    
    def __init__(self):
        super().__init__("xml")
    
    def extract_text_content(self, file_path: str) -> str:
        try:
            with open(file_path, 'rb') as f:
                raw_data = f.read()
                encoding = chardet.detect(raw_data)['encoding'] or 'utf-8'
            
            tree = ET.parse(file_path)
            root = tree.getroot()
            text = self._get_all_text(root)
            
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            cleaned_text = ' '.join(chunk for chunk in chunks if chunk)
            
            return cleaned_text
        
        except Exception as e:
            print(f"Error extracting text from {file_path}: {e}")
            return ""
    
    def _get_all_text(self, element: ET.Element) -> str:
        text = element.text or ""
        for child in element:
            text += self._get_all_text(child)
            if child.tail:
                text += child.tail
        return text
    
    def extract_sections(self, file_path: str) -> List[str]:
        try:
            with open(file_path, 'rb') as f:
                raw_data = f.read()
                encoding = chardet.detect(raw_data)['encoding'] or 'utf-8'
            
            tree = ET.parse(file_path)
            root = tree.getroot()
            
            sections = []
            for element in root.iter():
                text = (element.text or "").strip()
                if text and len(text) > 10:
                    section_text = f"{element.tag}: {text}"
                    lines = (line.strip() for line in section_text.splitlines())
                    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
                    cleaned_text = ' '.join(chunk for chunk in chunks if chunk)
                    if cleaned_text:
                        sections.append(cleaned_text)
            
            if not sections:
                full_text = self.extract_text_content(file_path)
                if full_text:
                    sections = [full_text]
            
            return sections
        
        except Exception as e:
            print(f"Error extracting sections from {file_path}: {e}")
            return [self.extract_text_content(file_path)]
    
    def parse_file(self, file_path: str, uploaded_by: str = "") -> Dict[str, Any]:
        """Parse an XML file and return structured + unstructured format"""
        try:
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"File not found: {file_path}")
            
            # Extract sections (XML elements with text)
            sections = self.extract_sections(file_path)
            
            # Generate file ID once for consistency
            file_id = self.generate_file_id()
            
            # Create structured data (each XML element as separate post)
            structured = []
            for section in sections:
                structured.append(self.create_post(file_id, section))
            
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
