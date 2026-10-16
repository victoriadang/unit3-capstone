import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

conn = psycopg2.connect(
    host=os.getenv("RDS_HOST"), port=int(os.getenv("RDS_PORT")), 
    dbname=os.getenv("RDS_DATABASE"), 
    user=os.getenv("RDS_USER"), 
    password=os.getenv("RDS_PASSWORD")
)
cur = conn.cursor()
print("RDS row counts:")
for table in ["clients", "projects", "consultants", "invoices"]:
    cur.execute(f"SELECT COUNT(*) FROM {table}")
    print(f"    {table}: {cur.fetchone()[0]}")
conn.close()

from agents.retrieval_agent import get_opensearch_client
client = get_opensearch_client()
print("OpenSearch document count:", client.count(index="documents")["count"])

from agents.sql_agent import run_sql_agent
from agents.retrieval_agent import run_retrieval_agent

print("SQL Keys:    ", sorted(run_sql_agent("How many active projects do we have?").keys()))
print("Retrieval Keys:", sorted(run_retrieval_agent("What is our onboarding process?").keys()))