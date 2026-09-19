"""
Stage 2 of the pipeline: splitting documents into chunks.

⚠️ THIS IS THE FILE YOU CHANGE IN MILESTONE 3.

`split_documents` below is deliberately plain. It cuts every document into
fixed-size pieces with a fixed overlap and pays no attention to where sentences
or paragraphs end. It works, and it is not good.

On a corpus of short posts it may not cut anything at all: `campus_life` comes
out as 88 documents and 88 chunks, because almost nothing in it reaches 800
characters. That is the baseline, not a bug — Milestone 3 is where you decide
whether one post should stay one chunk.

Your job in Milestone 3 is to replace the *body* of `split_documents` with a
strategy that fits the documents you actually read in Milestone 1. Keep the
name and the shape of what it returns — the rest of the pipeline calls it, and
your README has to name the function that produced your chunks.

If you get stuck for 30 minutes, `fallback_split` is the original. Switch back
to it, write down what you saw, and move on. That's a real observation about
your pipeline, not giving up.
"""

from dataclasses import dataclass

import config
import re
from ingest import Document
_SENTENCE_SPLIT = re.compile(r"(?<=[.!?])\s+")
_PARAGRAPH_SPLIT = re.compile(r"\n\s*\n")

@dataclass
class Chunk:
    """One piece of one document."""

    text: str
    source: str        # which file it came from
    index: int         # which chunk within that file, starting at 0
    produced_by: str   # the function that made it — cite this in your README

    @property
    def label(self) -> str:
        return f"{self.source}#{self.index}"


def fallback_split(
    documents: list[Document],
    chunk_size: int | None = None,
    overlap: int | None = None,
) -> list[Chunk]:
    """
    The starter's original chunker. Fixed-size character windows with overlap.

    Keep this function. Milestone 3's stop rule points back at it, and having
    something to compare your own strategy against is useful in unit 2.
    """
    chunk_size = chunk_size or config.CHUNK_SIZE
    overlap = overlap or config.CHUNK_OVERLAP

    if overlap >= chunk_size:
        raise ValueError("overlap has to be smaller than chunk_size")

    chunks: list[Chunk] = []
    for doc in documents:
        start = 0
        index = 0
        while start < len(doc.text):
            piece = doc.text[start : start + chunk_size].strip()
            if piece:
                chunks.append(
                    Chunk(
                        text=piece,
                        source=doc.source,
                        index=index,
                        produced_by="chunker.py::fallback_split",
                    )
                )
                index += 1
            start += chunk_size - overlap

    return chunks


def split_documents(
    documents: list[Document],
    target_min: int = 250,
    target_max: int = 400,
    hard_cap: int = 700,
) -> list[Chunk]:
    """
    Splits on paragraph/ sentence boundaries, trageting 250-400 characters.
    Falls back to a hard character cut only when a single sentence exceeds
    hard_cap. Overlap carries the last sentence of a chunk into the next.
    """

    chunks: list[Chunk] = []

    for doc in documents:
        paragraphs = [p.strip() for p in _PARAGRAPH_SPLIT.split(doc.text) if p.strip()]
        index = 0
        current = ""

        def emit(text: str):
            nonlocal index
            text = text.strip()
            if text:
                chunks.append(
                    Chunk(
                        text=text,
                        source=doc.source,
                        index=index,
                        produced_by="chunker.py::split_documents",
                    )
                )
                index += 1
        
        for para in paragraphs:
            sentences = [s.strip() for s in _SENTENCE_SPLIT.split(para) if s.strip()]

            for sent in sentences:
                # A single sentence longer than hard_cap gets hard-cut on its own -
                # this should be rare; it's the fallback, not the default path.
		
                if len(sent) > hard_cap:
                    if current:
                        emit(current)
                        current = ""
                    start = 0
                    while start < len(sent):
                        piece = sent[start : start + hard_cap]
                        emit(piece)
                        start += hard_cap
                    continue

                candidate = f"{current} {sent}".strip() if current else sent

                if len(candidate) <= target_max:
                    current = candidate
                else:
                    # Current chunk is full - emit it, then start the next one
                    # by carrying its last sentence forward as overlap
                    emit(current)
                    last_sentence = _SENTENCE_SPLIT.split(current)[-1]
                    current = f"{last_sentence} {sent}".strip()
	
            # Prefer to end a chunk at a paragraph boundary once it's already
            # hit the target_min, rather than dragging the next topic into it.
            if current and len(current) >= target_min:
                emit(current)
                current = ""
        
        if current:
            emit(current)

    return chunks 


 
    """
    Split documents into chunks. ⚠️ REPLACE THE BODY OF THIS IN MILESTONE 3.

    Right now it just calls the fallback. That is the plain, generic behaviour
    the brief is talking about.

    When you write your own strategy, set `produced_by` to
    "chunker.py::split_documents" so your README's Sample Chunks section names
    the right function. `app.py chunks` prints that string for you.

    Things worth thinking about before you write any code:
      - Are your documents short posts or long guides?
      - Is the useful information in one sentence, or spread over a paragraph?
      - Would splitting on paragraph breaks keep more thoughts intact than
        splitting on a character count?
    """
    return fallback_split(documents)


def describe(chunks: list[Chunk]) -> str:
    """A one-line summary, printed after indexing."""
    if not chunks:
        return "0 chunks"
    lengths = [len(c.text) for c in chunks]
    return (
        f"{len(chunks)} chunks, "
        f"{sum(lengths) // len(lengths)} characters on average "
        f"(shortest {min(lengths)}, longest {max(lengths)}), "
        f"produced by {chunks[0].produced_by}"
    )


if __name__ == "__main__":
    from ingest import load_documents

    chunks = split_documents(load_documents())
    print(describe(chunks))
