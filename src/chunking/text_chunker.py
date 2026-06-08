class TextChunker:

    def __init__(
        self,
        chunk_size=1000
    ):
        self.chunk_size = chunk_size

    def split_text(
        self,
        text: str
    ):

        paragraphs = text.split("\n")

        chunks = []

        current_chunk = ""

        for paragraph in paragraphs:

            if len(
                current_chunk
            ) + len(
                paragraph
            ) < self.chunk_size:

                current_chunk += (
                    paragraph + "\n"
                )

            else:

                chunks.append(
                    current_chunk.strip()
                )

                current_chunk = (
                    paragraph + "\n"
                )

        if current_chunk:

            chunks.append(
                current_chunk.strip()
            )

        return chunks