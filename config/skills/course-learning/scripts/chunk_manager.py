#!/usr/bin/env python3
"""
Chunk Manager for Large PDF Processing.

Manages intelligent chunking strategies for different processing modes.
Handles chunk sizing, overlap, and cross-chunk context preservation.
"""

from dataclasses import dataclass, field
from typing import Optional
import json
import sys

from pdf_preprocessor import PDFMetadata, analyze_pdf


@dataclass
class ChunkConfig:
    """Configuration for chunking strategy."""

    mode: str
    base_chunk_size: int
    overlap_pages: int = 2
    max_tokens: int = 30000
    respect_boundaries: bool = True


@dataclass
class Chunk:
    """A single chunk of PDF content."""

    chunk_id: int
    start_page: int
    end_page: int
    overlap_start: int
    overlap_end: int
    estimated_tokens: int
    is_first: bool = False
    is_last: bool = False
    context_from_previous: Optional[str] = None

    @property
    def total_pages(self) -> int:
        """Total pages including overlap."""
        return self.overlap_end - self.overlap_start + 1

    @property
    def core_pages(self) -> int:
        """Core pages excluding overlap."""
        return self.end_page - self.start_page + 1

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "chunk_id": self.chunk_id,
            "start_page": self.start_page,
            "end_page": self.end_page,
            "overlap_start": self.overlap_start,
            "overlap_end": self.overlap_end,
            "estimated_tokens": self.estimated_tokens,
            "is_first": self.is_first,
            "is_last": self.is_last,
        }


@dataclass
class ChunkPlan:
    """Complete chunking plan for a PDF."""

    pdf_path: str
    mode: str
    total_pages: int
    total_chunks: int
    chunks: list[Chunk] = field(default_factory=list)
    config: Optional[ChunkConfig] = None

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "pdf_path": self.pdf_path,
            "mode": self.mode,
            "total_pages": self.total_pages,
            "total_chunks": self.total_chunks,
            "chunks": [c.to_dict() for c in self.chunks],
            "config": {
                "base_chunk_size": self.config.base_chunk_size,
                "overlap_pages": self.config.overlap_pages,
                "max_tokens": self.config.max_tokens,
            } if self.config else None,
        }


MODE_CONFIGS = {
    "summary": ChunkConfig(
        mode="summary",
        base_chunk_size=10,
        overlap_pages=2,
        max_tokens=30000,
        respect_boundaries=True,
    ),
    "homework": ChunkConfig(
        mode="homework",
        base_chunk_size=5,
        overlap_pages=2,
        max_tokens=25000,
        respect_boundaries=True,
    ),
    "review": ChunkConfig(
        mode="review",
        base_chunk_size=15,
        overlap_pages=2,
        max_tokens=35000,
        respect_boundaries=True,
    ),
}


def get_chunk_config(mode: str, custom_chunk_size: Optional[int] = None) -> ChunkConfig:
    """
    Get chunking configuration for a mode.

    Args:
        mode: Processing mode (summary, homework, review)
        custom_chunk_size: Optional custom chunk size

    Returns:
        ChunkConfig for the mode
    """
    config = MODE_CONFIGS.get(mode, MODE_CONFIGS["summary"])

    if custom_chunk_size:
        return ChunkConfig(
            mode=mode,
            base_chunk_size=custom_chunk_size,
            overlap_pages=config.overlap_pages,
            max_tokens=config.max_tokens,
            respect_boundaries=config.respect_boundaries,
        )

    return config


def create_chunk_plan(
    pdf_path: str,
    mode: str = "summary",
    custom_chunk_size: Optional[int] = None,
    page_range: Optional[tuple[int, int]] = None,
) -> ChunkPlan:
    """
    Create a complete chunking plan for a PDF.

    Args:
        pdf_path: Path to the PDF file
        mode: Processing mode
        custom_chunk_size: Optional custom chunk size
        page_range: Optional (start, end) page range to process

    Returns:
        ChunkPlan with all chunks defined
    """
    metadata = analyze_pdf(pdf_path)
    config = get_chunk_config(mode, custom_chunk_size)

    start_page = page_range[0] if page_range else 1
    end_page = page_range[1] if page_range else metadata.total_pages

    start_page = max(1, min(start_page, metadata.total_pages))
    end_page = max(start_page, min(end_page, metadata.total_pages))

    plan = ChunkPlan(
        pdf_path=pdf_path,
        mode=mode,
        total_pages=end_page - start_page + 1,
        total_chunks=0,
        config=config,
    )

    chunks = _generate_chunks(
        metadata=metadata,
        config=config,
        start_page=start_page,
        end_page=end_page,
    )

    plan.chunks = chunks
    plan.total_chunks = len(chunks)

    return plan


def _generate_chunks(
    metadata: PDFMetadata,
    config: ChunkConfig,
    start_page: int,
    end_page: int,
) -> list[Chunk]:
    """Generate chunks based on configuration and PDF structure."""
    chunks = []
    current_start = start_page
    chunk_id = 0

    while current_start <= end_page:
        chunk_end = min(current_start + config.base_chunk_size - 1, end_page)

        if config.respect_boundaries and metadata.chapter_boundaries:
            for boundary in metadata.chapter_boundaries:
                if current_start < boundary <= chunk_end + 2:
                    if boundary > current_start:
                        chunk_end = boundary - 1
                    break

        overlap_start = max(start_page, current_start - config.overlap_pages)
        overlap_end = min(end_page, chunk_end + config.overlap_pages)

        if current_start == start_page:
            overlap_start = start_page

        estimated_tokens = _estimate_chunk_tokens(
            metadata, overlap_start, overlap_end
        )

        while estimated_tokens > config.max_tokens and chunk_end > current_start:
            chunk_end -= 1
            overlap_end = min(end_page, chunk_end + config.overlap_pages)
            estimated_tokens = _estimate_chunk_tokens(
                metadata, overlap_start, overlap_end
            )

        chunk = Chunk(
            chunk_id=chunk_id,
            start_page=current_start,
            end_page=chunk_end,
            overlap_start=overlap_start,
            overlap_end=overlap_end,
            estimated_tokens=estimated_tokens,
            is_first=(current_start == start_page),
            is_last=(chunk_end >= end_page),
        )

        chunks.append(chunk)
        chunk_id += 1
        current_start = chunk_end + 1

    return chunks


def _estimate_chunk_tokens(
    metadata: PDFMetadata,
    start_page: int,
    end_page: int,
) -> int:
    """Estimate tokens for a page range."""
    if not metadata.pages:
        chars_per_page = metadata.total_chars / max(1, metadata.total_pages)
        page_count = end_page - start_page + 1
        return int((chars_per_page * page_count) / 3.5)

    total = 0
    for page in metadata.pages:
        if start_page <= page.page_num <= end_page:
            total += page.estimated_tokens

    return total


def get_chunk_read_range(chunk: Chunk, include_overlap: bool = True) -> tuple[int, int]:
    """
    Get the page range to read for a chunk.

    Args:
        chunk: The chunk to read
        include_overlap: Whether to include overlap pages

    Returns:
        (start_page, end_page) tuple
    """
    if include_overlap:
        return (chunk.overlap_start, chunk.overlap_end)
    return (chunk.start_page, chunk.end_page)


def format_chunk_context(
    chunk: Chunk,
    previous_summary: Optional[str] = None,
) -> str:
    """
    Format context information for processing a chunk.

    Args:
        chunk: The chunk to process
        previous_summary: Summary from previous chunk

    Returns:
        Formatted context string
    """
    context_parts = [
        f"## Chunk {chunk.chunk_id + 1} Context",
        f"- Core pages: {chunk.start_page}-{chunk.end_page}",
        f"- Reading pages: {chunk.overlap_start}-{chunk.overlap_end} (with overlap)",
        f"- Estimated tokens: {chunk.estimated_tokens:,}",
    ]

    if chunk.is_first:
        context_parts.append("- Position: FIRST chunk")
    elif chunk.is_last:
        context_parts.append("- Position: LAST chunk")

    if previous_summary:
        context_parts.extend([
            "",
            "### Context from Previous Chunk:",
            previous_summary,
        ])

    return "\n".join(context_parts)


def needs_chunking(pdf_path: str, threshold_pages: int = 30) -> bool:
    """
    Determine if a PDF needs chunking.

    Args:
        pdf_path: Path to the PDF file
        threshold_pages: Page threshold for chunking

    Returns:
        True if chunking is needed
    """
    try:
        metadata = analyze_pdf(pdf_path)
        return metadata.total_pages > threshold_pages
    except Exception:
        return False


def print_chunk_plan(plan: ChunkPlan) -> None:
    """Print formatted chunk plan."""
    print(f"\n{'='*60}")
    print(f"Chunk Plan: {plan.pdf_path}")
    print(f"{'='*60}")
    print(f"Mode: {plan.mode}")
    print(f"Total Pages: {plan.total_pages}")
    print(f"Total Chunks: {plan.total_chunks}")

    if plan.config:
        print(f"\nConfiguration:")
        print(f"  Base chunk size: {plan.config.base_chunk_size} pages")
        print(f"  Overlap: {plan.config.overlap_pages} pages")
        print(f"  Max tokens: {plan.config.max_tokens:,}")

    print(f"\nChunks:")
    for chunk in plan.chunks:
        flags = []
        if chunk.is_first:
            flags.append("FIRST")
        if chunk.is_last:
            flags.append("LAST")
        flag_str = f" [{', '.join(flags)}]" if flags else ""

        print(f"  #{chunk.chunk_id + 1}: Pages {chunk.start_page}-{chunk.end_page} "
              f"(read {chunk.overlap_start}-{chunk.overlap_end}) "
              f"~{chunk.estimated_tokens:,} tokens{flag_str}")

    print(f"\n{'='*60}")


def main():
    """CLI entry point."""
    if len(sys.argv) < 2:
        print("Usage: python chunk_manager.py <pdf_path> [mode] [--json]")
        print("Modes: summary (default), homework, review")
        sys.exit(1)

    pdf_path = sys.argv[1]
    mode = "summary"
    output_json = "--json" in sys.argv

    for arg in sys.argv[2:]:
        if arg in MODE_CONFIGS:
            mode = arg

    try:
        if needs_chunking(pdf_path):
            plan = create_chunk_plan(pdf_path, mode)

            if output_json:
                print(json.dumps(plan.to_dict(), indent=2))
            else:
                print_chunk_plan(plan)
        else:
            print(f"PDF does not need chunking (< 30 pages)")
            metadata = analyze_pdf(pdf_path)
            print(f"Total pages: {metadata.total_pages}")

    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
