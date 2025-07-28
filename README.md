# Challenge 1b: Persona-Driven Multi-Collection PDF Analysis

## Overview

This project provides an advanced, automated solution for analyzing multiple collections of PDF documents. The system processes each collection based on a specific persona and use case defined in a corresponding input file. It extracts and ranks the most relevant sections and sub-sections, delivering a structured JSON output tailored to each collection's unique requirements.

The architecture is designed to be scalable and generic, capable of handling diverse domains—from travel planning and technical tutorials to recipe analysis—without code modification.

---

## Solution Explanation & Methodology

The solution employs a modular, multi-stage pipeline orchestrated by the main execution script (`main.py`).

1.  **Collection Discovery**: The script begins by scanning the `Challenge_1b/` directory for individual collection folders. It then iterates through each one to perform a targeted analysis.

2.  **Input Parsing**: For each collection, the system reads the `challenge1b_input.json` file to load the specific persona, the job-to-be-done, and the list of PDF documents to be processed.

3.  **Document Processing (`document_processor.py`)**: The listed PDFs are processed to extract raw text and identify structural elements. A heuristic-based approach detects section titles using formatting cues like numbering, capitalization, and keywords, breaking the document into logical chunks.

4.  **Persona & Job Analysis (`persona_analyzer.py`)**: The system analyzes the persona and job descriptions from the input file. It uses NLP techniques to extract key requirements, identify the user's domain (e.g., academic, technical), and determine priority keywords. This step is crucial for tailoring the analysis to the user's specific context.

5.  **Relevance Scoring (`relevance_scorer.py`)**: Each document section is scored for relevance against the user's requirements.
    * **TF-IDF Vectorization**: Sections are converted into numerical vectors to represent their term importance.
    * **Cosine Similarity**: The system measures the semantic similarity between each section and the user's needs.
    * **Comprehensive Ranking**: The final importance rank is determined by a weighted score that considers text similarity, section length, and title relevance.

6.  **Sub-section Analysis (`subsection_analyzer.py`)**: The highest-scoring sections undergo a more granular analysis. They are broken down into smaller sub-sections (paragraphs or sentence groups), which are then scored and ranked individually to provide the most precise and relevant content snippets.

---

## Models and Libraries Used

The solution is designed to be lightweight and CPU-only, utilizing a combination of standard machine learning and NLP libraries.

* **Models**:
    * **`en_core_web_sm` (from spaCy)**: A small, efficient, pre-trained English language model used for NLP tasks like named entity recognition (NER) and noun phrase extraction. Its small footprint (~50MB) makes it ideal for meeting the project's size constraints.

* **Libraries**:
    * **`scikit-learn`**: The core machine learning library used for implementing the TF-IDF vectorizer and calculating cosine similarity for the relevance scoring engine.
    * **`spaCy` & `NLTK`**: A suite of NLP libraries used for text processing tasks, including tokenization (splitting text into words and sentences), part-of-speech tagging, and stop-word removal. Fallback mechanisms are included in the code to handle cases where NLTK data packages might be missing.
    * **`pdfplumber`**: A robust library for extracting text and structural information from PDF documents with high fidelity.
    * **`numpy` & `pandas`**: Used for efficient numerical operations and data manipulation during the scoring process.

---

## Project Structure

The project is organized into a main directory containing the Python scripts and a `Challenge_1b` directory that holds the individual collections.

```
.
├── Challenge_1b/
│   ├── Collection 1/
│   │   ├── PDFs/
│   │   │   └── document1.pdf
│   │   └── challenge1b_input.json
│   ├── Collection 2/
│   │   ├── PDFs/
│   │   │   └── document2.pdf
│   │   └── challenge1b_input.json
│   └── ... (and so on)
├── main.py
├── document_processor.py
├── persona_analyzer.py
├── relevance_scorer.py
├── subsection_analyzer.py
├── requirements.txt
├── Dockerfile
└── README.md
```

---

## Execution Instructions

The recommended method for running this solution is with Docker, as it ensures a consistent and reliable environment.

1.  **Build the Docker Image**:
    Navigate to the project's root directory in your terminal and run the following command:
    ```bash
    docker build --platform linux/amd64 -t multi-collection-analyzer:latest .
    ```

2.  **Run the Container**:
    This command will start the application. The script will automatically discover and process all collections located inside the `Challenge_1b` directory.
    ```bash
    docker run --rm --network none multi-collection-analyzer:latest
    ```
    The results for each collection will be saved as a `challenge1b_output.json` file within their respective folders inside the container.
