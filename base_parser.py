import uuid
from datetime import datetime, timezone
from typing import List, Dict, Any

class BaseParser:
    def __init__(self, source_type: str):
        self.source_type = source_type
        self.source = "internal_data"
    
    def generate_file_id(self) -> str:
        return str(uuid.uuid4()).replace("-", "")
    
    def create_post(self, file_id: str, text: str) -> Dict[str, Any]:
        return {
            "pid": str(uuid.uuid4()),
            "file_id": file_id,
            "text": text,
            "source": self.source,
            "source_type": self.source_type,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    
    def create_combined_output(self, file_path: str, sections: List[str]) -> List[Dict[str, Any]]:
        file_id = self.generate_file_id()
        posts = [self.create_post(file_id, section) for section in sections]
        
        # Add full text as last post
        full_text = ' '.join(sections)
        if full_text:
            posts.append(self.create_post(file_id, full_text))
        
        return posts
