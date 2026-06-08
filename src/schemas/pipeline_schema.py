from pydantic import BaseModel
from typing import List, Optional

class Chunk(BaseModel):
    chunk_id: str
    document_id: str
    chunk_index: int
    page: int
    source_file: str
    char_count: int
    word_count: int
    text: str
    embedding: Optional[list] = None


class WikiDocument(BaseModel):
    document_id: str
    file_name: str
    file_type: str
    created_at: str

    chunks: List[Chunk]