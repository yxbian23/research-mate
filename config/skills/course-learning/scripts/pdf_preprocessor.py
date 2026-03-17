#!/usr/bin/env python3
"""
PDF Preprocessor for Large PDF Handling.

Analyzes PDF structure to enable intelligent chunking for the /course command.
Extracts metadata, TOC, page count, and estimates token usage.
"""

from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional
import json
import sys


@dataclass
class PageInfo:
    """Information about a single PDF page."""

    page_num: int
    char_count: int
    has_images: bool = False
    has_tables: bool = False
    has_formulas: bool = False
    estimated_tokens: int = 0


@dataclass
class TOCEntry:
    """Table of contents entry."""

    title: str
    page_num: int
    level: int


@dataclass
class PDFMetadata:
    """Complete PDF metadata for chunking decisions."""

    file_path: str
    total_pages: int
    title: Optional[str] = None
    author: Optional[str] = None
    toc: list[TOCEntry] = field(default_factory=list)
    pages: list[PageInfo] = field(default_factory=list)
    total_chars: int = 0
    estimated_total_tokens: int = 0
    content_dense_pages: list[int] = field(default_factory=list)
    chapter_boundaries: list[int] = field(default_factory=list)

    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization."""
        return {
            "file_path": self.file_path,
            "total_pages": self.total_pages,
            "title": self.title,
            "author": self.author,
            "toc": [
                {"title": e.title, "page_num": e.page_num, "level": e.level}
                for e in self.toc
            ],
            "total_chars": self.total_chars,
            "estimated_total_tokens": self.estimated_total_tokens,
            "content_dense_pages": self.content_dense_pages,
            "chapter_boundaries": self.chapter_boundaries,
        }


def estimate_tokens_from_chars(char_count: int) -> int:
    """
    Estimate token count from character count.

    Uses a conservative ratio: ~4 chars per token for English,
    ~2 chars per token for mixed content with formulas.
    """
    return int(char_count / 3.5)


def analyze_pdf(pdf_path: str) -> PDFMetadata:
    """
    Analyze PDF structure and extract metadata.

    Args:
        pdf_path: Path to the PDF file

    Returns:
        PDFMetadata with complete analysis
    """
    path = Path(pdf_path)
    if not path.exists():
        raise FileNotFoundError(f"PDF not found: {pdf_path}")

    try:
        import pypdf

        reader = pypdf.PdfReader(str(path))
    except ImportError:
        try:
            import PyPDF2

            reader = PyPDF2.PdfReader(str(path))
        except ImportError:
            return _analyze_pdf_fallback(pdf_path)

    total_pages = len(reader.pages)
    metadata = PDFMetadata(
        file_path=str(path.absolute()),
        total_pages=total_pages,
    )

    if reader.metadata:
        metadata.title = reader.metadata.get("/Title")
        metadata.author = reader.metadata.get("/Author")

    metadata.toc = _extract_toc(reader)

    total_chars = 0
    for i, page in enumerate(reader.pages):
        text = page.extract_text() or ""
        char_count = len(text)
        total_chars += char_count

        has_formulas = _detect_formulas(text)
        has_tables = _detect_tables(text)

        page_info = PageInfo(
            page_num=i + 1,
            char_count=char_count,
            has_formulas=has_formulas,
            has_tables=has_tables,
            estimated_tokens=estimate_tokens_from_chars(char_count),
        )
        metadata.pages.append(page_info)

        if has_formulas or has_tables or char_count > 3000:
            metadata.content_dense_pages.append(i + 1)

    metadata.total_chars = total_chars
    metadata.estimated_total_tokens = estimate_tokens_from_chars(total_chars)
    metadata.chapter_boundaries = _find_chapter_boundaries(metadata)

    return metadata


def _extract_toc(reader) -> list[TOCEntry]:
    """Extract table of contents from PDF outline."""
    toc = []

    try:
        if hasattr(reader, "outline") and reader.outline:
            _parse_outline(reader.outline, toc, level=0, reader=reader)
    except Exception:
        pass

    return toc


def _parse_outline(outline, toc: list[TOCEntry], level: int, reader) -> None:
    """Recursively parse PDF outline."""
    for item in outline:
        if isinstance(item, list):
            _parse_outline(item, toc, level + 1, reader)
        else:
            try:
                title = item.title if hasattr(item, "title") else str(item.get("/Title", ""))
                page_num = 1

                if hasattr(item, "page"):
                    page_idx = reader.get_destination_page_number(item)
                    page_num = page_idx + 1 if page_idx is not None else 1

                toc.append(TOCEntry(title=title, page_num=page_num, level=level))
            except Exception:
                continue


def _detect_formulas(text: str) -> bool:
    """Detect if page contains mathematical formulas."""
    formula_indicators = [
        "\\sum", "\\int", "\\frac", "\\sqrt",
        "∑", "∫", "∂", "∇", "∞",
        "≤", "≥", "≠", "≈",
        "argmax", "argmin",
        "P(", "E[", "Var(",
    ]
    return any(ind in text for ind in formula_indicators)


def _detect_tables(text: str) -> bool:
    """Detect if page contains tables."""
    lines = text.split("\n")
    pipe_count = sum(1 for line in lines if "|" in line)
    tab_count = sum(1 for line in lines if "\t" in line)
    return pipe_count >= 3 or tab_count >= 3


def _find_chapter_boundaries(metadata: PDFMetadata) -> list[int]:
    """Find chapter/section boundaries from TOC or content."""
    boundaries = [1]

    if metadata.toc:
        for entry in metadata.toc:
            if entry.level == 0 and entry.page_num not in boundaries:
                boundaries.append(entry.page_num)
    else:
        chunk_size = max(10, metadata.total_pages // 5)
        for i in range(chunk_size, metadata.total_pages, chunk_size):
            boundaries.append(i + 1)

    boundaries.sort()
    return boundaries


def _analyze_pdf_fallback(pdf_path: str) -> PDFMetadata:
    """
    Fallback analysis when pypdf is not available.

    Uses basic file info and heuristics.
    """
    path = Path(pdf_path)
    file_size = path.stat().st_size

    estimated_pages = max(1, file_size // 50000)
    estimated_chars = file_size // 2

    return PDFMetadata(
        file_path=str(path.absolute()),
        total_pages=estimated_pages,
        total_chars=estimated_chars,
        estimated_total_tokens=estimate_tokens_from_chars(estimated_chars),
    )


def get_toc(pdf_path: str) -> list[TOCEntry]:
    """
    Extract table of contents from PDF.

    Args:
        pdf_path: Path to the PDF file

    Returns:
        List of TOC entries
    """
    metadata = analyze_pdf(pdf_path)
    return metadata.toc


def estimate_tokens(pdf_path: str, start_page: int = 1, end_page: Optional[int] = None) -> int:
    """
    Estimate token count for specified page range.

    Args:
        pdf_path: Path to the PDF file
        start_page: Starting page (1-indexed)
        end_page: Ending page (inclusive), None for all remaining

    Returns:
        Estimated token count
    """
    metadata = analyze_pdf(pdf_path)

    if end_page is None:
        end_page = metadata.total_pages

    start_idx = max(0, start_page - 1)
    end_idx = min(len(metadata.pages), end_page)

    return sum(p.estimated_tokens for p in metadata.pages[start_idx:end_idx])


def get_optimal_chunks(
    pdf_path: str,
    mode: str = "summary",
    max_tokens_per_chunk: int = 30000,
) -> list[tuple[int, int]]:
    """
    Get optimal page ranges for chunking.

    Args:
        pdf_path: Path to the PDF file
        mode: Processing mode (summary, homework, review)
        max_tokens_per_chunk: Maximum tokens per chunk

    Returns:
        List of (start_page, end_page) tuples
    """
    metadata = analyze_pdf(pdf_path)

    base_chunk_sizes = {
        "summary": 10,
        "homework": 5,
        "review": 15,
    }
    base_size = base_chunk_sizes.get(mode, 10)

    chunks = []
    current_start = 1
    current_tokens = 0

    for page in metadata.pages:
        if current_tokens + page.estimated_tokens > max_tokens_per_chunk:
            if current_start <= page.page_num - 1:
                chunks.append((current_start, page.page_num - 1))
            current_start = page.page_num
            current_tokens = page.estimated_tokens
        else:
            current_tokens += page.estimated_tokens

            pages_in_chunk = page.page_num - current_start + 1
            if pages_in_chunk >= base_size:
                if page.page_num in metadata.chapter_boundaries:
                    chunks.append((current_start, page.page_num))
                    current_start = page.page_num + 1
                    current_tokens = 0

    if current_start <= metadata.total_pages:
        chunks.append((current_start, metadata.total_pages))

    return chunks


def print_analysis(metadata: PDFMetadata) -> None:
    """Print formatted analysis results."""
    print(f"\n{'='*60}")
    print(f"PDF Analysis: {Path(metadata.file_path).name}")
    print(f"{'='*60}")
    print(f"Total Pages: {metadata.total_pages}")
    print(f"Total Characters: {metadata.total_chars:,}")
    print(f"Estimated Tokens: {metadata.estimated_total_tokens:,}")

    if metadata.title:
        print(f"Title: {metadata.title}")
    if metadata.author:
        print(f"Author: {metadata.author}")

    if metadata.toc:
        print(f"\nTable of Contents ({len(metadata.toc)} entries):")
        for entry in metadata.toc[:10]:
            indent = "  " * entry.level
            print(f"  {indent}Page {entry.page_num}: {entry.title}")
        if len(metadata.toc) > 10:
            print(f"  ... and {len(metadata.toc) - 10} more entries")

    if metadata.content_dense_pages:
        print(f"\nContent-dense pages: {metadata.content_dense_pages[:20]}")

    if metadata.chapter_boundaries:
        print(f"Chapter boundaries: {metadata.chapter_boundaries}")

    print(f"\n{'='*60}")


def main():
    """CLI entry point."""
    if len(sys.argv) < 2:
        print("Usage: python pdf_preprocessor.py <pdf_path> [--json]")
        sys.exit(1)

    pdf_path = sys.argv[1]
    output_json = "--json" in sys.argv

    try:
        metadata = analyze_pdf(pdf_path)

        if output_json:
            print(json.dumps(metadata.to_dict(), indent=2))
        else:
            print_analysis(metadata)

            print("\nOptimal chunks by mode:")
            for mode in ["summary", "homework", "review"]:
                chunks = get_optimal_chunks(pdf_path, mode)
                print(f"  {mode}: {chunks}")

    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error analyzing PDF: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
