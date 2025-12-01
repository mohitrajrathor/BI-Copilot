from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import create_sql_agent
import pandas as pd
from app.core.config import config
from app.utils.charting import generate_chart
import json

class AnalyticsAgent:
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key=config.GOOGLE_API_KEY)
        self.db = SQLDatabase.from_uri(config.DATABASE_URL)
        self.agent_executor = create_sql_agent(
            llm=self.llm,
            toolkit=None, # We might need to pass toolkit if we want more control, but create_sql_agent handles it with db
            db=self.db,
            agent_type="zero-shot-react-description",
            verbose=True
        )

    def process_query(self, query: str):
        # 1. Get data using SQL Agent
        # Note: The SQL agent returns a string answer. We might need to intercept the intermediate steps or ask it to return data.
        # For a hackathon, we can ask it to return the SQL query, then execute it ourselves to get the DF.
        
        # Let's try a different approach: Ask LLM to generate SQL, then we execute.
        from langchain.chains import create_sql_query_chain
        
        chain = create_sql_query_chain(self.llm, self.db)
        sql_query = chain.invoke({"question": query})
        
        # Clean SQL (sometimes it returns markdown)
        sql_query = sql_query.replace("```sql", "").replace("```", "").strip()
        
        try:
            # Execute SQL
            result = self.db.run(sql_query)
            # The result from db.run is string, we want raw results for dataframe
            # We can use the engine directly
            from sqlalchemy import text
            with self.db._engine.connect() as connection:
                df = pd.read_sql(text(sql_query), connection)
            
            # 2. Analyze data and decide on chart
            # We can ask LLM what chart to generate based on columns
            # For simplicity, let's use a heuristic or a simple LLM call
            
            chart_type = "bar" # Default
            if len(df) > 0:
                columns = df.columns.tolist()
                # Simple heuristic: if 2 columns, one string one number -> bar
                # if time series -> line
                
                # Let's ask LLM for chart config
                prompt = f"Given the dataframe columns {columns} and the user query '{query}', suggest a chart type (bar, line, scatter, pie) and which columns to use for x and y. Return JSON like {{'chart_type': 'bar', 'x_col': 'col1', 'y_col': 'col2'}}"
                response = self.llm.invoke(prompt)
                try:
                    content = response.content.replace("```json", "").replace("```", "").strip()
                    chart_config = json.loads(content)
                except:
                    chart_config = {"chart_type": "bar", "x_col": columns[0], "y_col": columns[1] if len(columns) > 1 else columns[0]}

                chart_image = generate_chart(
                    df, 
                    chart_type=chart_config.get("chart_type", "bar"),
                    x_col=chart_config.get("x_col"),
                    y_col=chart_config.get("y_col"),
                    title=query
                )
                
                return {
                    "answer": f"Here is the analysis for: {query}",
                    "sql": sql_query,
                    "table": df.head().to_html(classes="table table-striped"),
                    "chart": chart_image
                }
            else:
                return {"answer": "No data found for this query.", "sql": sql_query}

        except Exception as e:
            return {"answer": f"Error processing query: {str(e)}", "sql": sql_query}

analytics_agent = AnalyticsAgent()
