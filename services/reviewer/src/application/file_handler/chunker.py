import tiktoken

from src.domain.interfaces.chunker import IChunkerService


class ChunkerService(IChunkerService):
    def __init__(self, model: str = "gpt-4o-mini") -> None:
        self.max_tokens = 0
        self._model = model
        self._tokenizer = tiktoken.encoding_for_model(model)

    def chunk(self, files: dict[str, str], max_tokens: float) -> list[str]:
        self.max_tokens = max_tokens
        chunks = []
        current_chunk_lines = []
        current_tokens = 0

        for path, content in files.items():
            prefix = f"\n\n(PATH: {path})"
            prefix_tokens = len(self._tokenizer.encode(prefix))

            if current_tokens + prefix_tokens > self.max_tokens:
                if current_chunk_lines:
                    chunks.append("".join(current_chunk_lines))

                current_chunk_lines = []
                current_tokens = 0

            current_chunk_lines.append(prefix)
            current_tokens += prefix_tokens

            for line in content.splitlines():
                if not line.strip():
                    continue

                line_tokens = len(self._tokenizer.encode(line))

                if line_tokens > self.max_tokens:
                    split_chunks = self._split_line(line)
                    for sc in split_chunks:
                        sc_tokens = len(self._tokenizer.encode(sc))
                        if current_tokens + sc_tokens > self.max_tokens:
                            chunks.append("".join(current_chunk_lines))
                            current_chunk_lines = [prefix, sc]
                            current_tokens = prefix_tokens + sc_tokens
                        else:
                            current_chunk_lines.append(sc)
                            current_tokens += sc_tokens
                    continue

                if current_tokens + line_tokens > self.max_tokens:
                    chunks.append("".join(current_chunk_lines))
                    current_chunk_lines = [prefix, line]
                    current_tokens = prefix_tokens + line_tokens
                else:
                    current_chunk_lines.append("\n" + line)
                    current_tokens += line_tokens + 1

        if current_chunk_lines:
            chunks.append("".join(current_chunk_lines))

        return chunks

    def _split_line(self, text: str) -> list[str]:
        words = text.split()
        chunks = []
        current_words = []
        current_tokens = 0

        for word in words:
            word_tokens = len(self._tokenizer.encode(word))
            if current_tokens + word_tokens > self.max_tokens:
                chunks.append(" ".join(current_words))
                current_words = [word]
                current_tokens = word_tokens
            else:
                current_words.append(word)
                current_tokens += word_tokens

        if current_words:
            chunks.append(" ".join(current_words))

        return chunks
