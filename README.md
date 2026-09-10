# AI Student Support Assistant

A beginner-friendly Python terminal application for answering common student
questions from a local knowledge base. The project demonstrates query
handling, lightweight information retrieval, document processing, and optional
OCR for scanned notices.

## Features

- Natural-language questions in a terminal interface
- Keyword-based retrieval from `student_data.txt`
- Exam, guidelines, library, fees, attendance, and contact resources
- Optional OCR for image-based notices with Tesseract
- `reload`, `help`, `ocr`, and `exit` commands
- Unit tests for the retrieval workflow
- No API key or internet connection required for normal questions

## Project structure

```text
ai-student-support-assistant/
├── main.py
├── ocr_module.py
├── student_data.txt
├── test_assistant.py
├── requirements.txt
└── .gitignore
```

## Run the assistant

1. Install Python 3.9 or newer.
2. Create and activate a virtual environment (recommended).
3. Install optional OCR dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Start the application:

   ```bash
   python main.py
   ```

Example questions:

```text
What is the exam schedule?
What are the student guidelines?
When is the library open?
How do I contact the accounts office?
```

## OCR setup

The Python package `pytesseract` is a bridge to the Tesseract OCR program.
Install Tesseract separately for your operating system, then run:

```text
ocr path/to/examination_notice.png
```

If OCR is not installed, the assistant still works normally for text-based
student resources.

## Run tests

```bash
python -m unittest -v
```

## How it works

The assistant splits the knowledge base into named resources, tokenizes the
student's question, scores matching resources, and returns the highest-ranked
answer. This is a transparent local retrieval workflow rather than a
cloud-based large language model, which makes it easy to demonstrate and
customize during an internship project.

## Future enhancements

- Web interface with Flask or FastAPI
- Database-backed notices and student accounts
- Tamil/English multilingual support
- A large language model for richer answers
- Voice input and automatic document uploads