from docx import Document


class DOCXParser:

    def extract_text(self, file_path: str):

        doc = Document(file_path)

        text = "\n".join(
            para.text
            for para in doc.paragraphs
            if para.text.strip()
        )

        return [{
            "page": 1,
            "text": text
        }]