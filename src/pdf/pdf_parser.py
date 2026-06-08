import fitz


class PDFParser:

    def extract_text(self, file_path: str):

        doc = fitz.open(file_path)

        chunks = []

        for page_num in range(len(doc)):

            page = doc[page_num]

            text = page.get_text()

            chunks.append({
                "page": page_num + 1,
                "text": text
            })

        doc.close()

        return chunks