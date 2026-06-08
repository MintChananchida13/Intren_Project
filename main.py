from src.ingestion.router import Router

from src.pdf.pdf_parser import PDFParser
from src.docx.docx_parser import DOCXParser

from src.metadata.metadata_manager import MetadataManager
from src.chunking.text_chunker import TextChunker

from src.exporter.json_exporter import JSONExporter

from src.schemas.pipeline_schema import (
    Chunk,
    WikiDocument
)

INPUT_FILE = "data/input/my_document_DOCX.docx"

OUTPUT_FILE = "data/output/wiki_data.json"


router = Router()

file_type = router.get_file_type(
    INPUT_FILE
)

if file_type == "pdf":

    parser = PDFParser()

elif file_type == "docx":

    parser = DOCXParser()

else:

    raise ValueError("Unsupported")


raw_chunks = parser.extract_text(
    INPUT_FILE
)


metadata = MetadataManager.create_document_metadata(
    INPUT_FILE
)


chunker = TextChunker(
    chunk_size=1000
)


processed_chunks = []

chunk_counter = 1


for page_data in raw_chunks:

    page = page_data["page"]

    text = page_data["text"]

    text_chunks = chunker.split_text(
        text
    )

    for chunk_text in text_chunks:

        processed_chunks.append(Chunk(
    chunk_id=f"chunk_{chunk_counter}",

    document_id=metadata["document_id"],

    chunk_index=chunk_counter,

    page=page,

    source_file=metadata["file_name"],

    char_count=len(chunk_text),

    word_count=len(chunk_text.split()),

    text=chunk_text
)
)

        chunk_counter += 1


document = WikiDocument(
    document_id=metadata["document_id"],
    file_name=metadata["file_name"],
    file_type=metadata["file_type"],
    created_at=metadata["created_at"],
    chunks=processed_chunks
)


exporter = JSONExporter()

exporter.export(
    document,
    OUTPUT_FILE
)

print("Done")