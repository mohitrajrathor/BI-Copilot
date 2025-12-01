# BI-Copilot

BI-Copilot is an AI-powered Business Intelligence assistant designed to help users analyze data, generate visualizations, and derive insights using natural language queries.

## Features

- **Natural Language Querying**: Ask questions about your data in plain English.
- **Automated Visualization**: Generate charts and graphs automatically based on your data.
- **Data Analysis**: Get summary statistics and insights.
- **Interactive Dashboard**: User-friendly interface built with Streamlit.

## Tech Stack

- **Frontend**: [Streamlit](https://streamlit.io/)
- **Backend**: Python
- **AI/LLM**: LangChain / OpenAI (or similar)
- **Data Processing**: Pandas

## Project Structure

```
bi-agent/
├── backend/        # Backend logic and API handling
├── frontend/       # Streamlit frontend application
├── .gitignore      # Git ignore rules
└── README.md       # Project documentation
```

## Getting Started

### Prerequisites

- Python 3.8+
- pip

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd bi-agent
   ```

2. **Set up a virtual environment**
   ```bash
   python -m venv venv
   # Windows
   .\venv\Scripts\activate
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
   *(Note: `requirements.txt` is coming soon)*

4. **Configure Environment Variables**
   - Create a `.env` file in the `backend` directory.
   - Add necessary API keys (e.g., `OPENAI_API_KEY`).

### Running the Application

To run the Streamlit app:

```bash
streamlit run frontend/app.py
```
*(Note: Ensure `frontend/app.py` exists or update the path to your main Streamlit script)*
