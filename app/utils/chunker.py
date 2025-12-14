import tiktoken

def chunk_text(text: str, max_tokens: int = 50, overlap: int = 10) -> list[str]:
    enc = tiktoken.get_encoding("cl100k_base")

    tokens = enc.encode(text)
    chunks = []

    start = 0

    while start < len(tokens):
        end = start + max_tokens
        chunk_tokens = tokens[start:end]
        chunk_text = enc.decode(chunk_tokens)
        chunks.append(chunk_text)
        start += max_tokens - overlap

    return chunks
