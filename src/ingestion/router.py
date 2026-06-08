from pathlib import Path


class Router:

    def get_file_type(self, file_path: str):

        ext = Path(file_path).suffix.lower()

        if ext == ".pdf":
            return "pdf"

        if ext == ".docx":
            return "docx"

        raise ValueError(
            f"Unsupported file type: {ext}"
        )