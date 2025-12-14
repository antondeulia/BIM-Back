import tiktoken
import re

def chunk_text(
    text: str,
    max_tokens: int = 200,
    overlap_tokens: int = 50
) -> list[str]:

    enc = tiktoken.get_encoding("cl100k_base")

    sentences = re.split(r'(?<=[.!?])\s+', text.strip())

    chunks = []
    current_chunk = []
    current_tokens = 0

    for sentence in sentences:
        sent_tokens = len(enc.encode(sentence))

        if sent_tokens > max_tokens:
            subchunks = []
            tokens = enc.encode(sentence)

            for i in range(0, len(tokens), max_tokens - overlap_tokens):
                sub = enc.decode(tokens[i:i + max_tokens])
                subchunks.append(sub)

            chunks.extend(subchunks)
            continue

        if current_tokens + sent_tokens > max_tokens:
            chunks.append(" ".join(current_chunk))

            if overlap_tokens > 0:
                overlap = enc.decode(
                    enc.encode(" ".join(current_chunk))[-overlap_tokens:]
                )
                current_chunk = [overlap]
                current_tokens = len(enc.encode(overlap))
            else:
                current_chunk = []
                current_tokens = 0

        current_chunk.append(sentence)
        current_tokens += sent_tokens

    if current_chunk:
        chunks.append(" ".join(current_chunk))

    return chunks
