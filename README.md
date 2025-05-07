# AI Resume Builder with ATS Scoring

An AI-powered resume builder that generates professionally formatted resumes in Markdown format optimized for Applicant Tracking Systems (ATS). The application uses Meta's Llama-4-Scout model via Groq's API and LangChain framework to analyze job descriptions and generate tailored resume content.

## Features

- AI-powered resume content generation
- ATS scoring and analysis
- Markdown resume output
- Job description analysis
- Resume storage and management
- Improvement suggestions

## Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd resume-builder
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the root directory with your API keys:
```
GROQ_API_KEY=your_groq_api_key_here
```

5. Run the Streamlit app:
```bash
streamlit run app.py
```

## Project Structure

- `app.py`: Main Streamlit application
- `config.py`: Configuration and environment variables
- `resume_generator/`: Core resume generation logic
  - `llm_utils.py`: LLM integration utilities
  - `ats_scorer.py`: ATS scoring implementation
  - `markdown_formatter.py`: Markdown formatting utilities
- `api/`: FastAPI implementation
  - `main.py`: API endpoints
  - `models.py`: Pydantic models
- `tests/`: Test files

## Development

This project is built with:
- Streamlit for the web interface
- LangChain for LLM integration
- Groq API for Llama-4-Scout model access
- FastAPI for the REST API
- Pydantic for data validation
