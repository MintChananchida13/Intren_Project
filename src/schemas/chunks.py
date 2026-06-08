from dataclasses import dataclass
from typing import List, Literal


# =========================
# BASE
# =========================
@dataclass
class BaseChunk:
    chunk_id: str
    document_id: str
    chunk_index: int
    page: int
    source_file: str
    char_count: int
    word_count: int
    chunk_type: str


# =========================
# TEXT CHUNK
# =========================
@dataclass
class TextChunk(BaseChunk):
    chunk_type: Literal["TEXT"]
    text: str


# =========================
# TABLE CHUNK
# =========================
@dataclass
class TableChunk(BaseChunk):
    chunk_type: Literal["TABLE"]
    text: str  # markdown table

    table_rows: int
    table_columns: int

    flatten_text: str  # 🔥 RAG embedding optimized


# =========================
# UNION TYPE
# =========================
Chunk = TextChunk | TableChunk