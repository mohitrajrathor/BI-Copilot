# BI-Copilot: GenAI-Powered Data Analysis System

A production-ready, multi-agent AI system for analyzing databases using natural language. Built with FastAPI, React, and Google Gemini.

## 🎯 Key Features

- **Natural Language Queries** - Ask questions in plain English
- **4-Agent Pipeline** - Orchestrator → Analysis Planner → SQL Generator → Dashboard Generator
- **Database Safety** - Read-only connections, SQL injection protection, automatic LIMIT enforcement
- **Smart Caching** - Redis-powered caching at every layer (schema, plans, results, LLM responses)
- **Modern UI** - Clean React interface with Recharts visualizations
- **Multiple Chart Types** - KPI cards, line charts, bar charts, pie charts, scatter plots, tables

## 🏗️ Architecture

```
User Query
    ↓
[Agent 1: Orchestrator] ─→ Classify intent (trend/comparison/summary/exploration)
    ↓
[Agent 2: Analysis Planner] ─→ Convert to structured JSON plan (metrics, dimensions, filters)
    ↓
[Agent 3: SQL Generator] ─→ Template-based SQL generation + safe execution
    ↓
[Agent 4: Dashboard Generator] ─→ Deterministic chart selection + dashboard spec
    ↓
Frontend Renders Dashboard
```

**Safety First:**
- ✅ Read-only database connections
- ✅ SQL keyword blacklist (INSERT, UPDATE, DELETE, DROP, etc.)
- ✅ Automatic query timeout and row limits
- ✅ All queries logged
- ✅ No raw SQL from users

**Performance:**
- ⚡ Schema cached permanently in Redis
- ⚡ Query plans cached by intent hash
- ⚡ SQL results cached with TTL
- ⚡ LLM responses cached
- ⚡ Small model (Gemini Flash) for classification
- ⚡ Large model (Gemini Pro) only for planning

## 📋 Prerequisites

- **Python 3.10+**
- **Node.js 18+**
- **Redis** (via Docker or local installation)
- **Google Gemini API Key** ([Get one here](https://ai.google.dev/))
- **Database** (SQLite for testing, PostgreSQL/MySQL for production)

## 🚀 Quick Start

### 1. Clone and Setup

```bash
git clone <repository-url>
cd BI-Copilot
```

### 2. Start Redis

```bash
docker-compose up -d redis
```

### 3. Backend Setup

```bash
cd backend

# Install dependencies (using uv or pip)
pip install -r requirements.txt

# Create .env file
cp .env.example .env

# Edit .env and add your Gemini API key
# GEMINI_API_KEY=your_key_here

# Create sample database
python create_sample_db.py

# Start backend server
uvicorn main:app --reload
# Backend runs on http://localhost:8000
```

### 4. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Start frontend development server
npm run dev
# Frontend runs on http://localhost:5173
```

### 5. Test the Application

1. Open http://localhost:5173 in your browser
2. Try example queries like:
   - "Show me total sales by region"
   - "What are the top 10 products by revenue?"
   - "Plot monthly sales trends"
   - "Compare product categories"

## 📁 Project Structure

```
BI-Copilot/
├── backend/
│   ├── app/
│   │   ├── agents/           # 4 agent implementations
│   │   │   ├── orchestrator.py
│   │   │   ├── analysis_planner.py
│   │   │   ├── sql_generator.py
│   │   │   └── dashboard_generator.py
│   │   ├── core/             # Core infrastructure
│   │   │   ├── config.py
│   │   │   ├── database.py
│   │   │   ├── cache.py
│   │   │   └── schema.py
│   │   ├── routes/           # API endpoints
│   │   │   ├── analyze.py
│   │   │   ├── schema_routes.py
│   │   │   └── health.py
│   │   └── utils/            # Utilities
│   │       ├── sql_templates.py
│   │       └── chart_mapper.py
│   ├── main.py               # FastAPI application
│   ├── create_sample_db.py   # Sample database script
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/       # React components
│   │   │   ├── QueryInput.tsx
│   │   │   ├── ProgressTracker.tsx
│   │   │   ├── DashboardRenderer.tsx
│   │   │   └── ChartComponents.tsx
│   │   ├── hooks/            # Custom hooks
│   │   │   └── useAnalysis.ts
│   │   ├── lib/              # API client & types
│   │   │   ├── api.ts
│   │   │   └── types.ts
│   │   └── App.tsx
│   └── package.json
└── docker-compose.yml        # Redis & PostgreSQL services
```

## 🔧 Configuration

### Backend (.env)

```env
GEMINI_API_KEY=your_api_key
REDIS_URL=redis://localhost:6379
DATABASE_URL=sqlite+aiosqlite:///./test.db

# Safety limits
QUERY_TIMEOUT_SECONDS=30
MAX_ROWS=10000

# LLM models
CLASSIFICATION_MODEL=gemini-1.5-flash
PLANNING_MODEL=gemini-1.5-pro

# Caching
CACHE_TTL_SECONDS=3600
SCHEMA_CACHE_PERMANENT=true

# Features
ENABLE_QUERY_LOGGING=true
ENABLE_INSIGHTS=true
```

### Frontend (.env)

```env
VITE_API_URL=http://localhost:8000
```

## 📊 API Endpoints

### `POST /api/analyze`
Main analysis endpoint.

**Request:**
```json
{
  "query": "Show me sales by region"
}
```

**Response:**
```json
{
  "intent": "comparison",
  "plan": {
    "table": "sales",
    "metrics": [...],
    "dimensions": [...]
  },
  "sql": "SELECT ...",
  "data": {
    "columns": [...],
    "rows": [...]
  },
  "dashboard_spec": {
    "title": "Sales by Region",
    "charts": [...],
    "insight": "..."
  }
}
```

### `GET /api/schema/info`
Get database schema information.

### `GET /api/health`
Health check endpoints (also `/api/health/redis`, `/api/health/database`).

Visit http://localhost:8000/docs for interactive API documentation.

## 🧪 Testing

### Sample Queries to Try

**Trend Analysis:**
- "Show sales trends over time"
- "Plot monthly revenue"

**Comparison:**
- "Compare sales by region"
- "Show top customers by revenue"

**Summary:**
- "Total sales and revenue"
- "Average order value"

**Exploration:**
- "Top 10 products"
- "Find highest spending customers"

### Testing Safety Features

The system will block these queries:
- "DELETE FROM sales"
- "UPDATE sales SET ..."
- "DROP TABLE sales"

## 🎨 Customization

### Add New Chart Types

Edit `backend/app/utils/chart_mapper.py` to add chart type logic.
Edit `frontend/src/components/ChartComponents.tsx` to add React components.

### Change LLM Models

Update `CLASSIFICATION_MODEL` and `PLANNING_MODEL` in `.env`.

### Custom Database

Update `DATABASE_URL` in `.env` to your database connection string.

## 🐛 Troubleshooting

**Redis Connection Error:**
```bash
docker-compose up -d redis
# Or install Redis locally
```

**Gemini API Error:**
- Check your API key in `.env`
- Verify at https://ai.google.dev/

**Database Connection Error:**
- Verify `DATABASE_URL` format
- For PostgreSQL: `postgresql+asyncpg://user:pass@host/db`
- For MySQL: `mysql+aiomysql://user:pass@host/db`

## 📈 Performance Optimization

The system follows these principles:

1. **Cache Everything** - Schema, plans, results, LLM responses
2. **Use Small Models** - Fast classification with Gemini Flash
3. **Deterministic Logic** - Chart selection uses rules, not AI
4. **Async Everywhere** - Full async/await architecture
5. **Template-Based SQL** - No LLM for SQL generation

**Expected Latency:**
- First query: < 5 seconds (cold cache)
- Repeated query: < 500ms (warm cache)

## 🔒 Security

- ❌ No database writes allowed
- ❌ No raw SQL from users
- ❌ No SQL comments
- ❌ No multiple statements
- ✅ Read-only connections
- ✅ Query logging
- ✅ Automatic timeouts

## 📝 License

MIT

## 🤝 Contributing

Contributions welcome! Please open an issue or PR.

---

Built with ❤️ using FastAPI, React, and Google Gemini
