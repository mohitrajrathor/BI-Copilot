# BI-Copilot

BI-Copilot is an AI-powered Business Intelligence assistant that enables business users to analyze data and generate visualizations using natural language queries. The system leverages Google's Gemini LLM to automatically generate SQL queries, execute them safely, and create insightful dashboards—all without requiring any technical knowledge from the user.

## Features

- **Natural Language to SQL**: Converts plain English questions into SQL queries using Google Gemini
- **Automated Visualization**: Generates charts (bar, line, scatter, pie) automatically based on query results
- **Interactive Chat Interface**: Vue.js-based chat UI for seamless user interaction
- **Real-time Analytics**: Processes data with pandas and displays KPIs and insights
- **Dashboard Generation**: Creates complete HTML dashboards with charts and data tables
- **Multi-Database Support**: Works with PostgreSQL, MySQL, BigQuery, and SQLite

## Tech Stack

- **Frontend**: Vue.js 3 + TypeScript + Vite
- **Backend**: FastAPI (Python)
- **AI/LLM**: Google Gemini (via LangChain)
- **Database**: SQLAlchemy (supports PostgreSQL, MySQL, BigQuery, SQLite)
- **Data Processing**: Pandas
- **Visualization**: Matplotlib

## Project Structure

```
bi-copilot/
├── backend/
│   ├── app/
│   │   ├── agents/
│   │   │   └── analytics_agent.py    # LangChain + Gemini integration
│   │   ├── core/
│   │   │   ├── config.py             # Configuration management
│   │   │   └── database.py           # Database connection
│   │   ├── routers/
│   │   │   └── chat.py               # API endpoints
│   │   └── utils/
│   │       └── charting.py           # Matplotlib chart generation
│   ├── main.py                       # FastAPI application
│   ├── requirements.txt              # Python dependencies
│   └── .env                          # Environment variables
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── ChatInterface.vue     # Chat UI component
│   │   │   └── Dashboard.vue         # Dashboard display component
│   │   ├── App.vue                   # Main application
│   │   └── main.ts                   # Entry point
│   ├── package.json                  # Node dependencies
│   └── vite.config.ts                # Vite configuration
├── .gitignore
└── README.md
```

## Getting Started

### Prerequisites

- **Python 3.8+**
- **Node.js 16+** and npm
- **Google Gemini API Key** ([Get one here](https://ai.google.dev/))
- **Database** (PostgreSQL, MySQL, BigQuery, or SQLite)

### Installation

#### 1. Clone the Repository

```bash
git clone <repository-url>
cd bi-copilot
```

#### 2. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create a virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# Windows:
.\venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install database driver (if using PostgreSQL)
pip install psycopg2
```

#### 3. Configure Environment Variables

Create a `.env` file in the `backend` directory:

```env
GOOGLE_API_KEY=your_gemini_api_key_here
DATABASE_URL=your_database_connection_string

# Examples:
# PostgreSQL: postgresql://user:password@localhost:5432/dbname
# MySQL: mysql://user:password@localhost:3306/dbname
# SQLite: sqlite:///./test.db
# BigQuery: bigquery://project-id/dataset-id
```

#### 4. Frontend Setup

```bash
# Navigate to frontend directory (from project root)
cd frontend

# Install dependencies
npm install
```

### Running the Application

You need to run both the backend and frontend servers.

#### Start the Backend Server

```bash
# From the backend directory
cd backend

# Activate virtual environment if not already active
# Windows:
.\venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Start the FastAPI server
uvicorn main:app --reload

# Server will run on http://localhost:8000
```

#### Start the Frontend Server

```bash
# From the frontend directory (in a new terminal)
cd frontend

# Start the development server
npm run dev

# Server will run on http://localhost:5173 (or similar)
```

### Using the Application

1. Open your browser and navigate to the frontend URL (typically `http://localhost:5173`)
2. Type a natural language query in the chat interface, for example:
   - "Show me total sales by region"
   - "What are the top 10 customers by revenue?"
   - "Plot monthly revenue trends"
3. The system will:
   - Generate the appropriate SQL query
   - Execute it against your database
   - Create visualizations
   - Display results in an interactive dashboard

## API Documentation

Once the backend is running, visit `http://localhost:8000/docs` for interactive API documentation (Swagger UI).

### Main Endpoint

**POST** `/api/chat`

Request body:
```json
{
  "query": "Show me sales by region"
}
```

Response:
```json
{
  "answer": "Here is the analysis for: Show me sales by region",
  "sql": "SELECT region, SUM(sales) FROM sales_table GROUP BY region",
  "table": "<html table>",
  "chart": "base64_encoded_image"
}
```

## Troubleshooting

### Backend Issues

- **ModuleNotFoundError: No module named 'psycopg2'**: Install the PostgreSQL driver with `pip install psycopg2`
- **Google Auth Error**: Ensure your `GOOGLE_API_KEY` is set correctly in the `.env` file
- **Database Connection Error**: Verify your `DATABASE_URL` is correct and the database is accessible

### Frontend Issues

- **CORS Error**: The backend is configured to allow all origins for development. If you encounter CORS issues, check the CORS middleware in `backend/main.py`
- **Connection Refused**: Ensure the backend server is running on `http://localhost:8000`

## Development

### Adding New Chart Types

Edit `backend/app/utils/charting.py` to add new visualization types.

### Customizing the Agent

Modify `backend/app/agents/analytics_agent.py` to change how queries are processed or add new capabilities.

