#!/usr/bin/env python3
"""
Round 1B: Persona-Driven Document Intelligence - Multi-Collection
Main execution script for the Adobe Challenge

This script processes multiple document collections based on a given persona
and job-to-be-done, extracting and ranking the most relevant sections.

Usage:
    python main.py
"""

import json
import os
import time
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any

# Import our custom modules
from document_processor import DocumentProcessor
from persona_analyzer import PersonaJobAnalyzer
from relevance_scorer import RelevanceScorer
from subsection_analyzer import SubSectionAnalyzer


class PersonaDrivenDocumentIntelligence:
    """Main orchestrator class for the complete pipeline."""

    def __init__(self):
        self.document_processor = DocumentProcessor()
        self.persona_analyzer = PersonaJobAnalyzer()
        self.relevance_scorer = RelevanceScorer()
        self.subsection_analyzer = SubSectionAnalyzer()
        self.processing_start_time = None

    def process(self, pdf_paths: List[str], persona: Dict, job: Dict, output_path: str):
        """Main processing pipeline for a single collection."""
        self.processing_start_time = time.time()
        print(f"🚀 Starting Persona-Driven Document Intelligence Pipeline for {Path(output_path).parent.name}")

        # Step 1: Process documents
        print("📚 Step 1: Processing documents...")
        documents = self.document_processor.process_documents(pdf_paths)
        if not documents:
            print("❌ No documents were successfully processed. Skipping collection.")
            return

        # Step 2: Analyze persona and job from the new JSON structure
        print("🧑‍💼 Step 2: Analyzing persona and job requirements...")
        # Extract the text from the dictionary
        persona_text = persona.get('role', '')
        job_text = job.get('task', '')

        persona_analysis = self.persona_analyzer.analyze_persona(persona_text)
        job_analysis = self.persona_analyzer.analyze_job(job_text)
        requirements = self.persona_analyzer.combine_requirements(persona_analysis, job_analysis)

        # Step 3: Score relevance
        print("📊 Step 3: Scoring section relevance...")
        self.relevance_scorer.prepare_scoring(documents, requirements)
        scored_sections = self.relevance_scorer.calculate_relevance_scores(requirements)
        top_sections = self.relevance_scorer.extract_top_sections(scored_sections, top_n=10)

        # Step 4: Analyze sub-sections
        print("🔍 Step 4: Analyzing sub-sections...")
        sub_sections = self.subsection_analyzer.analyze_subsections(
            documents, top_sections, requirements, max_subsections=20
        )

        # Step 5: Generate output
        print("📄 Step 5: Generating output...")
        output_data = self._generate_output(documents, persona, job, top_sections, sub_sections)

        total_time = time.time() - self.processing_start_time
        print(f"🎉 Pipeline for {Path(output_path).parent.name} completed in {total_time:.2f}s\n")

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, indent=2, ensure_ascii=False)
        print(f"💾 Output saved to: {output_path}")

    def _generate_output(self, documents: Dict, persona: Dict, job: Dict,
                        top_sections: List[Dict], sub_sections: List[Dict]) -> Dict[str, Any]:
        """Generate the required JSON output format."""
        metadata = {
            "input_documents": list(documents.keys()),
            "persona": persona.get('role', ''),
            "job_to_be_done": job.get('task', '')
        }

        extracted_sections_output = []
        for section in top_sections:
            extracted_sections_output.append({
                "document": section['document'],
                "section_title": section['section_title'],
                "importance_rank": section['importance_rank'],
                "page_number": section['page_number']
            })

        subsection_analysis_output = []
        for subsection in sub_sections:
            subsection_analysis_output.append({
                "document": subsection['document'],
                "refined_text": subsection['refined_text'],
                "page_number": subsection['page_number']
            })

        return {
            "metadata": metadata,
            "extracted_sections": extracted_sections_output,
            "subsection_analysis": subsection_analysis_output
        }


def main():
    """Main execution function to process all collections."""
    # The root directory containing all collections
    base_dir = Path("./Challenge_1b")

    if not base_dir.exists():
        print(f"❌ Base directory '{base_dir}' not found. Please ensure your project has this structure.")
        return

    intelligence_system = PersonaDrivenDocumentIntelligence()

    # Find all collection directories
    collection_dirs = [d for d in base_dir.iterdir() if d.is_dir()]

    if not collection_dirs:
        print(f"🤷 No collection folders found inside '{base_dir}'.")
        return

    for collection_path in collection_dirs:
        print(f"--- Processing Collection: {collection_path.name} ---")
        input_json_path = collection_path / "challenge1b_input.json"
        pdf_dir = collection_path / "PDFs"
        output_json_path = collection_path / "challenge1b_output.json"

        if not input_json_path.exists():
            print(f"⚠️  'challenge1b_input.json' not found in {collection_path.name}. Skipping.")
            continue
        if not pdf_dir.exists():
            print(f"⚠️  'PDFs' directory not found in {collection_path.name}. Skipping.")
            continue

        # Read the input JSON
        with open(input_json_path, 'r', encoding='utf-8') as f:
            input_data = json.load(f)

        # Get data from the input JSON
        documents_info = input_data.get("documents", [])
        persona_data = input_data.get("persona", {})
        job_data = input_data.get("job_to_be_done", {})

        # Construct full paths to PDF files
        pdf_paths = [str(pdf_dir / doc["filename"]) for doc in documents_info]

        # Process this collection
        try:
            intelligence_system.process(pdf_paths, persona_data, job_data, str(output_json_path))
        except Exception as e:
            print(f"❌ An error occurred while processing {collection_path.name}: {e}")
            import traceback
            traceback.print_exc()


if __name__ == "__main__":
    main()