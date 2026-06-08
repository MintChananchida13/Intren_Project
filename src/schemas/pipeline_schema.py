from pydantic import BaseModel
from typing import List, Optional, Union


# =========================
# BASE (shared fields only)
# =========================
class BaseChunk(BaseModel):
    chunk_id: str
    document_id: str
    chunk_index: int
    chunk_type: str
    page: int
    source_file: str
    char_count: int
    word_count: int
    text: str
    embedding: Optional[list] = None


# =========================
# TEXT CHUNK (NO TABLE FIELDS)
# =========================
class TextChunk(BaseChunk):
    chunk_type: str = "TEXT"


# =========================
# TABLE CHUNK (CLEAN STRUCTURE)
# =========================
class TableChunk(BaseChunk):
    chunk_type: str = "TABLE"

    table_rows: int
    table_columns: int


# =========================
# DOCUMENT
# =========================
class WikiDocument(BaseModel):
    document_id: str
    file_name: str
    file_type: str
    created_at: str

    chunks: List[Union[TextChunk, TableChunk]]