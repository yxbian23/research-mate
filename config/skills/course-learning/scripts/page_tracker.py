#!/usr/bin/env python3
"""
Page Tracker for Cross-Chunk Reference Management.

Maintains concept-to-page mappings across chunks and supports
accurate source reference tracking for the /course command.
"""

from dataclasses import dataclass, field
from typing import Optional
from pathlib import Path
import json
import sys


@dataclass
class Reference:
    """A reference to a specific location in the PDF."""

    page_num: int
    section: Optional[str] = None
    context: Optional[str] = None
    chunk_id: Optional[int] = None

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "page_num": self.page_num,
            "section": self.section,
            "context": self.context,
            "chunk_id": self.chunk_id,
        }

    def format(self, include_section: bool = True) -> str:
        """Format as citation string."""
        parts = [f"Page {self.page_num}"]
        if include_section and self.section:
            parts.append(f"({self.section})")
        return " ".join(parts)


@dataclass
class Concept:
    """A concept with its references."""

    name: str
    english_name: Optional[str] = None
    category: str = "general"
    references: list[Reference] = field(default_factory=list)
    definition: Optional[str] = None
    first_occurrence: Optional[int] = None

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "name": self.name,
            "english_name": self.english_name,
            "category": self.category,
            "references": [r.to_dict() for r in self.references],
            "definition": self.definition,
            "first_occurrence": self.first_occurrence,
        }

    def add_reference(self, ref: Reference) -> None:
        """Add a reference, avoiding duplicates."""
        for existing in self.references:
            if existing.page_num == ref.page_num:
                if ref.context and not existing.context:
                    existing.context = ref.context
                return

        self.references.append(ref)

        if self.first_occurrence is None or ref.page_num < self.first_occurrence:
            self.first_occurrence = ref.page_num

    def get_primary_reference(self) -> Optional[Reference]:
        """Get the primary (first) reference."""
        if not self.references:
            return None
        return min(self.references, key=lambda r: r.page_num)

    def format_citation(self) -> str:
        """Format all references as citation."""
        if not self.references:
            return ""

        pages = sorted(set(r.page_num for r in self.references))

        if len(pages) == 1:
            return f"Page {pages[0]}"
        elif len(pages) <= 3:
            return f"Pages {', '.join(map(str, pages))}"
        else:
            return f"Pages {pages[0]}, {pages[1]}, ... {pages[-1]}"


@dataclass
class PageTracker:
    """Tracks concepts and references across PDF chunks."""

    pdf_path: str
    concepts: dict[str, Concept] = field(default_factory=dict)
    page_concepts: dict[int, list[str]] = field(default_factory=dict)
    current_chunk_id: int = 0
    chunk_summaries: dict[int, str] = field(default_factory=dict)

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "pdf_path": self.pdf_path,
            "concepts": {k: v.to_dict() for k, v in self.concepts.items()},
            "page_concepts": self.page_concepts,
            "chunk_summaries": self.chunk_summaries,
        }

    def add_concept(
        self,
        name: str,
        page_num: int,
        english_name: Optional[str] = None,
        category: str = "general",
        section: Optional[str] = None,
        context: Optional[str] = None,
        definition: Optional[str] = None,
    ) -> Concept:
        """
        Add or update a concept with a reference.

        Args:
            name: Concept name (Chinese or English)
            page_num: Page number where concept appears
            english_name: English name if different from name
            category: Concept category (theorem, definition, example, etc.)
            section: Section name
            context: Surrounding context
            definition: Concept definition

        Returns:
            The concept object
        """
        key = self._normalize_key(name)

        if key not in self.concepts:
            self.concepts[key] = Concept(
                name=name,
                english_name=english_name,
                category=category,
                definition=definition,
            )
        else:
            concept = self.concepts[key]
            if english_name and not concept.english_name:
                concept.english_name = english_name
            if definition and not concept.definition:
                concept.definition = definition

        ref = Reference(
            page_num=page_num,
            section=section,
            context=context,
            chunk_id=self.current_chunk_id,
        )
        self.concepts[key].add_reference(ref)

        if page_num not in self.page_concepts:
            self.page_concepts[page_num] = []
        if key not in self.page_concepts[page_num]:
            self.page_concepts[page_num].append(key)

        return self.concepts[key]

    def get_concept(self, name: str) -> Optional[Concept]:
        """Get a concept by name."""
        key = self._normalize_key(name)
        return self.concepts.get(key)

    def get_concepts_on_page(self, page_num: int) -> list[Concept]:
        """Get all concepts on a specific page."""
        keys = self.page_concepts.get(page_num, [])
        return [self.concepts[k] for k in keys if k in self.concepts]

    def get_concepts_in_range(self, start_page: int, end_page: int) -> list[Concept]:
        """Get all concepts in a page range."""
        concepts = set()
        for page in range(start_page, end_page + 1):
            for key in self.page_concepts.get(page, []):
                if key in self.concepts:
                    concepts.add(key)
        return [self.concepts[k] for k in concepts]

    def get_concepts_by_category(self, category: str) -> list[Concept]:
        """Get all concepts of a specific category."""
        return [c for c in self.concepts.values() if c.category == category]

    def set_chunk_summary(self, chunk_id: int, summary: str) -> None:
        """Store summary for a chunk."""
        self.chunk_summaries[chunk_id] = summary

    def get_chunk_summary(self, chunk_id: int) -> Optional[str]:
        """Get summary for a chunk."""
        return self.chunk_summaries.get(chunk_id)

    def get_context_for_chunk(self, chunk_id: int) -> str:
        """Get combined context from previous chunks."""
        context_parts = []

        for i in range(max(0, chunk_id - 2), chunk_id):
            if i in self.chunk_summaries:
                context_parts.append(f"### Chunk {i + 1} Summary\n{self.chunk_summaries[i]}")

        return "\n\n".join(context_parts)

    def merge_references(self) -> None:
        """Merge duplicate references across chunks."""
        for concept in self.concepts.values():
            unique_refs = {}
            for ref in concept.references:
                if ref.page_num not in unique_refs:
                    unique_refs[ref.page_num] = ref
                else:
                    existing = unique_refs[ref.page_num]
                    if ref.context and not existing.context:
                        existing.context = ref.context
                    if ref.section and not existing.section:
                        existing.section = ref.section

            concept.references = sorted(unique_refs.values(), key=lambda r: r.page_num)

    def generate_glossary(self) -> str:
        """Generate a glossary of all concepts."""
        lines = ["# Glossary", ""]

        categories = {}
        for concept in self.concepts.values():
            cat = concept.category
            if cat not in categories:
                categories[cat] = []
            categories[cat].append(concept)

        for category in ["theorem", "definition", "concept", "example", "general"]:
            if category not in categories:
                continue

            lines.append(f"## {category.title()}s")
            lines.append("")

            for concept in sorted(categories[category], key=lambda c: c.name):
                name_str = concept.name
                if concept.english_name and concept.english_name != concept.name:
                    name_str = f"{concept.name} ({concept.english_name})"

                citation = concept.format_citation()
                lines.append(f"- **{name_str}**: {citation}")

                if concept.definition:
                    lines.append(f"  - {concept.definition[:100]}...")

            lines.append("")

        return "\n".join(lines)

    def generate_page_index(self) -> str:
        """Generate a page-by-page concept index."""
        lines = ["# Page Index", ""]

        for page_num in sorted(self.page_concepts.keys()):
            concepts = self.get_concepts_on_page(page_num)
            if concepts:
                concept_names = [c.name for c in concepts]
                lines.append(f"- **Page {page_num}**: {', '.join(concept_names)}")

        return "\n".join(lines)

    def _normalize_key(self, name: str) -> str:
        """Normalize concept name for dictionary key."""
        return name.lower().strip()

    def start_chunk(self, chunk_id: int) -> None:
        """Start processing a new chunk."""
        self.current_chunk_id = chunk_id

    def end_chunk(self, summary: Optional[str] = None) -> None:
        """End processing current chunk."""
        if summary:
            self.set_chunk_summary(self.current_chunk_id, summary)


def create_tracker(pdf_path: str) -> PageTracker:
    """Create a new page tracker for a PDF."""
    return PageTracker(pdf_path=pdf_path)


def load_tracker(json_path: str) -> PageTracker:
    """Load a page tracker from JSON file."""
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    tracker = PageTracker(pdf_path=data["pdf_path"])

    for key, concept_data in data.get("concepts", {}).items():
        concept = Concept(
            name=concept_data["name"],
            english_name=concept_data.get("english_name"),
            category=concept_data.get("category", "general"),
            definition=concept_data.get("definition"),
        )

        for ref_data in concept_data.get("references", []):
            ref = Reference(
                page_num=ref_data["page_num"],
                section=ref_data.get("section"),
                context=ref_data.get("context"),
                chunk_id=ref_data.get("chunk_id"),
            )
            concept.references.append(ref)

        if concept.references:
            concept.first_occurrence = min(r.page_num for r in concept.references)

        tracker.concepts[key] = concept

    tracker.page_concepts = {
        int(k): v for k, v in data.get("page_concepts", {}).items()
    }
    tracker.chunk_summaries = {
        int(k): v for k, v in data.get("chunk_summaries", {}).items()
    }

    return tracker


def save_tracker(tracker: PageTracker, json_path: str) -> None:
    """Save a page tracker to JSON file."""
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(tracker.to_dict(), f, indent=2, ensure_ascii=False)


def print_tracker_summary(tracker: PageTracker) -> None:
    """Print a summary of the tracker."""
    print(f"\n{'='*60}")
    print(f"Page Tracker: {Path(tracker.pdf_path).name}")
    print(f"{'='*60}")
    print(f"Total concepts: {len(tracker.concepts)}")
    print(f"Pages with concepts: {len(tracker.page_concepts)}")
    print(f"Chunks processed: {len(tracker.chunk_summaries)}")

    categories = {}
    for concept in tracker.concepts.values():
        cat = concept.category
        categories[cat] = categories.get(cat, 0) + 1

    print(f"\nBy category:")
    for cat, count in sorted(categories.items()):
        print(f"  {cat}: {count}")

    print(f"\nSample concepts:")
    for concept in list(tracker.concepts.values())[:5]:
        citation = concept.format_citation()
        print(f"  - {concept.name}: {citation}")

    print(f"\n{'='*60}")


def main():
    """CLI entry point."""
    if len(sys.argv) < 2:
        print("Usage: python page_tracker.py <command> [args]")
        print("Commands:")
        print("  create <pdf_path>       - Create new tracker")
        print("  load <json_path>        - Load and display tracker")
        print("  glossary <json_path>    - Generate glossary")
        print("  index <json_path>       - Generate page index")
        sys.exit(1)

    command = sys.argv[1]

    try:
        if command == "create":
            if len(sys.argv) < 3:
                print("Error: pdf_path required", file=sys.stderr)
                sys.exit(1)

            tracker = create_tracker(sys.argv[2])
            print_tracker_summary(tracker)

        elif command == "load":
            if len(sys.argv) < 3:
                print("Error: json_path required", file=sys.stderr)
                sys.exit(1)

            tracker = load_tracker(sys.argv[2])
            print_tracker_summary(tracker)

        elif command == "glossary":
            if len(sys.argv) < 3:
                print("Error: json_path required", file=sys.stderr)
                sys.exit(1)

            tracker = load_tracker(sys.argv[2])
            print(tracker.generate_glossary())

        elif command == "index":
            if len(sys.argv) < 3:
                print("Error: json_path required", file=sys.stderr)
                sys.exit(1)

            tracker = load_tracker(sys.argv[2])
            print(tracker.generate_page_index())

        else:
            print(f"Unknown command: {command}", file=sys.stderr)
            sys.exit(1)

    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
