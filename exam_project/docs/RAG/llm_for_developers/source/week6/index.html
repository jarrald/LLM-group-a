from typing import List


def chunk_text(text: str, chunk_size: int = 800, overlap: int = 120) -> List[str]:
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
    if not paragraphs:
        return []

    chunks: List[str] = []
    current = ""

    for para in paragraphs:
        candidate = para if not current else current + "\n\n" + para
        if len(candidate) <= chunk_size:
            current = candidate
        else:
            if current:
                chunks.append(current.strip())
            if len(para) <= chunk_size:
                current = para
            else:
                start = 0
                step = max(1, chunk_size - overlap)
                while start < len(para):
                    end = start + chunk_size
                    piece = para[start:end].strip()
                    if piece:
                        chunks.append(piece)
                    start += step
                current = ""

    if current.strip():
        chunks.append(current.strip())

    cleaned: List[str] = []
    seen = set()
    for chunk in chunks:
        chunk = " ".join(chunk.split())
        if chunk and chunk not in seen:
            cleaned.append(chunk)
            seen.add(chunk)
    return cleaned
