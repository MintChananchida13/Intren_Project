from src.chunking.text_chunker import TextChunker
from src.docx.docx_parser import DOCXParser
from src.exporter.json_exporter import JSONExporter
from src.ingestion.router import Router
from src.metadata.metadata_manager import MetadataManager
from src.pdf.pdf_parser import PDFParser
from src.schemas.pipeline_schema import TextChunk, TableChunk, WikiDocument


INPUT_FILE = "data/input/my_document_DOCX.docx"
OUTPUT_FILE = "data/output/wiki_data.json"


# =========================
# 1. ROUTER
# =========================
router = Router()
file_type = router.get_file_type(INPUT_FILE)

parser = PDFParser() if file_type == "pdf" else DOCXParser()


# =========================
# 2. METADATA + PARSE
# =========================
metadata = MetadataManager.create_document_metadata(INPUT_FILE)

# ⭐ IMPORTANT: parser now must return dict format OR normalize
raw_chunks = parser.extract_text(INPUT_FILE)


# =========================
# 3. INIT
# =========================
chunker = TextChunker(chunk_size=1000)
processed_chunks = []
chunk_counter = 1


# =========================
# 4. PROCESS PIPELINE (SAFE MODE)
# =========================
for page_data in raw_chunks:

    # =====================
    # SAFE ACCESS (DICT ONLY)
    # =====================
    page = page_data["page"]
    chunk_type = page_data["type"]
    text = page_data["text"]

    # =====================
    # TABLE
    # =====================
    if chunk_type == "TABLE":

        chunk_obj = TableChunk(
            chunk_id=f"chunk_{chunk_counter}",
            document_id=metadata["document_id"],
            chunk_index=chunk_counter,

            chunk_type="TABLE",

            page=page,
            source_file=metadata["file_name"],

            char_count=len(text),
            word_count=len(text.split()),

            text=text,

            table_rows=page_data.get("table_rows"),
            table_columns=page_data.get("table_columns"),
        )

        processed_chunks.append(chunk_obj)
        chunk_counter += 1
        continue


    # =====================
    # TEXT (SPLIT)
    # =====================
    text_chunks = chunker.split_text(text)

    for chunk_text in text_chunks:

        chunk_obj = TextChunk(
            chunk_id=f"chunk_{chunk_counter}",
            document_id=metadata["document_id"],
            chunk_index=chunk_counter,

            chunk_type="TEXT",

            page=page,
            source_file=metadata["file_name"],

            char_count=len(chunk_text),
            word_count=len(chunk_text.split()),

            text=chunk_text,
        )

        processed_chunks.append(chunk_obj)
        chunk_counter += 1


# =========================
# 5. EXPORT
# =========================
document = WikiDocument(
    document_id=metadata["document_id"],
    file_name=metadata["file_name"],
    file_type=metadata["file_type"],
    created_at=metadata["created_at"],
    chunks=processed_chunks,
)

exporter = JSONExporter()
exporter.export(document, OUTPUT_FILE)

print("Done")