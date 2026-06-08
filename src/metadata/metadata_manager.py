from pathlib import Path
from datetime import datetime
import uuid


class MetadataManager:

    @staticmethod
    def create_document_metadata(
        file_path: str
    ):

        file = Path(file_path)

        return {
            "document_id": str(uuid.uuid4()),
            "file_name": file.name,
            "file_type": file.suffix,
            "created_at": datetime.now().isoformat()
        }

    @staticmethod
    def create_chunk_metadata(
        chunk_id: str,
        page: int,
        source_file: str
    ):

        return {
            "chunk_id": chunk_id,
            "page": page,
            "source_file": source_file
        }