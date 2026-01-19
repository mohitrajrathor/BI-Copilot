# BI-Copilot: GenAI-Powered Data Analysis System

## Description
A production-ready, multi-agent AI system for analyzing databases using natural language. Built with FastAPI, React, and Google Gemini, it allows users to ask questions in plain English and receive accurate data visualizations. The system prioritizes safety through read-only connections and strictly controlled SQL generation, while ensuring high performance via comprehensive Redis caching.

## Tech Stack
- **Languages**: Python 3.10+, TypeScript / JavaScript
- **Frameworks**: FastAPI, React, Vite
- **Containerization**: Docker
- **Cloud / DevOps**: Google Gemini API, Redis, SQLite (Testing), PostgreSQL / MySQL (Production)

## Architecture
The system uses a 4-agent pipeline to process user requests:

1. **Orchestrator**: Classifies user intent (trend, comparison, summary, etc.).
2. **Analysis Planner**: Converts intent into a structured JSON plan (metrics, dimensions).
3. **SQL Generator**: Generates safe SQL using predefined templates (no raw LLM-generated SQL).
4. **Dashboard Generator**: Deterministically selects the optimal visualization for the result set.

**Data Flow**:  
User Query → Agents → Database (Read-only) → Frontend Dashboard

## Features
- **Natural Language Interface**: Perform complex analytics using plain English queries.
- **Multi-Agent Engine**: Orchestrator, Planner, SQL Generator, and Dashboard Generator working in coordination.
- **Enterprise-Grade Safety**: Read-only DB access, SQL injection prevention, query limits, and keyword blacklisting.
- **High Performance**: Redis caching for schemas, query plans, SQL results, and LLM responses.
- **Rich Visualizations**: Auto-generated KPI cards, line, bar, pie, and scatter charts using Recharts.

## CI/CD Pipeline

Code → Build → Test → Docker → Deploy

*Currently optimized for local development and Docker-based containerization.*

## Setup & Installation

### Prerequisites
- Python 3.10+
- Node.js 18+
- Docker (for Redis)
- Google Gemini API Key

### Steps

```bash
   git clone https://github.com/mohitrajrathor/BI-Copilot.git
   

   cd backend
   pip install -r requirements.txt
   cp .env.example .env  # Add your GEMINI_API_KEY
   python create_sample_db.py
   uvicorn main:app --reload
   

   cd frontend
   npm install
   npm run dev

```

## Usage

1. Open your browser at `http://localhost:5173`.
2. Enter a query in the search bar, for example:

   * "Show total sales by region"
   * "Top 10 products by revenue"
   * "Plot monthly sales trends"
3. Explore the generated dashboards and visualizations.

## Screenshots / Demo

![Dashboard Screenshot](path/to/screenshot.png)
*(Replace with actual screenshots or demo link)*

## Challenges & Learnings

* **Safety**: Prevented LLM hallucinations from executing unsafe SQL using template-based query generation.
* **Latency**: Reduced multi-agent response time through aggressive Redis caching of intermediate outputs.
* **Consistency**: Ensured reliable chart rendering across diverse data shapes using deterministic visualization logic.

## Future Improvements

* **Authentication**: User accounts and saved query history.
* **Extended Database Support**: Snowflake, BigQuery, and Redshift connectors.
* **Advanced Analytics**: Forecasting and anomaly detection modules.

## Author

**Mohit Raj Rathor** | 
[LinkedIn](https://www.linkedin.com/in/mohitrajrathor/)
