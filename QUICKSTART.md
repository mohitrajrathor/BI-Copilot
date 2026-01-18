# Quick Start Guide

## 1. Start Redis
```bash
docker-compose up -d redis
```

## 2. Setup Backend
```bash
cd backend

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env and add your GEMINI_API_KEY

# Create sample database
python create_sample_db.py

# Start server
uvicorn main:app --reload
```

Backend will be running at http://localhost:8000

## 3. Setup Frontend
```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

Frontend will be running at http://localhost:5173

## 4. Test
Open http://localhost:5173 and try queries like:
- "Show me total sales by region"
- "Plot monthly revenue trends"
- "Top 10 products by sales"

## API Documentation
Visit http://localhost:8000/docs for interactive API documentation.

## Troubleshooting

**Redis not running:**
```bash
docker-compose up -d redis
```

**Missing GEMINI_API_KEY:**
1. Go to https://ai.google.dev/
2. Get an API key
3. Add to backend/.env: `GEMINI_API_KEY=your_key_here`

**Import errors:**
```bash
cd backend
pip install -r requirements.txt
```

```bash
cd frontend
npm install
```
