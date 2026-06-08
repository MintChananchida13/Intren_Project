from docx import Document


class DOCXParser:

    def extract_text(self, file_path: str):

        doc = Document(file_path)

        chunks = []

        # =========================
        # TEXT
        # =========================
        text = "\n".join(
            p.text.strip()
            for p in doc.paragraphs
            if p.text and p.text.strip()
        )

        if text:
            chunks.append({
                "page": 1,
                "type": "TEXT",
                "text": text
            })

        # =========================
        # TABLE
        # =========================
        for table in doc.tables:

            header, rows = self.extract_table_meta(table)

            if not rows:
                continue

            chunks.append({
                "page": 1,
                "type": "TABLE",
                "text": self.table_to_markdown(header, rows),

                "table_rows": len(rows),
                "table_columns": len(header),
            })

        return chunks

    # =========================
    def extract_table_meta(self, table):
        rows = [
            [cell.text.strip() for cell in row.cells]
            for row in table.rows
        ]

        if not rows:
            return [], []

        return rows[0], rows[1:]

    # =========================
    def table_to_markdown(self, header, rows):
        md = []

        md.append("| " + " | ".join(header) + " |")
        md.append("| " + " | ".join(["---"] * len(header)) + " |")

        for r in rows:
            md.append("| " + " | ".join(r) + " |")

        return "\n".join(md)