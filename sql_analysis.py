"""
sql_analysis.py
Runs the same 5 business questions using SQL (via SQLite + pandas)
Demonstrates SQL skills alongside Python for the resume.
"""

import pandas as pd
import sqlite3

# Load CSV into SQLite in-memory database
df = pd.read_csv("ai_tool_adoption.csv")
conn = sqlite3.connect(":memory:")
df.to_sql("ai_adoption", conn, index=False, if_exists="replace")

print("=" * 60)
print("SQL ANALYSIS — Increasing Usage of AI")
print("=" * 60)

queries = {
    "Q1: Top Industries by Average AI Adoption Rate": """
        SELECT Industry,
               ROUND(AVG("Adoption_Rate_%"), 2) AS avg_adoption_rate
        FROM   ai_adoption
        GROUP  BY Industry
        ORDER  BY avg_adoption_rate DESC;
    """,

    "Q2: Year-over-Year Growth in Total AI Users": """
        SELECT Year,
               ROUND(SUM("Number_of_Users_(Millions)"), 2) AS total_users_millions
        FROM   ai_adoption
        GROUP  BY Year
        ORDER  BY Year;
    """,

    "Q3: Most Adopted AI Tool Overall": """
        SELECT AI_Tool,
               ROUND(AVG("Adoption_Rate_%"), 2) AS avg_adoption_rate,
               ROUND(SUM("Number_of_Users_(Millions)"), 1) AS total_users_millions
        FROM   ai_adoption
        GROUP  BY AI_Tool
        ORDER  BY avg_adoption_rate DESC;
    """,

    "Q4: AI Adoption by Company Size": """
        SELECT Company_Size,
               ROUND(AVG("Adoption_Rate_%"), 2) AS avg_adoption_rate
        FROM   ai_adoption
        GROUP  BY Company_Size
        ORDER  BY avg_adoption_rate DESC;
    """,

    "Q5: Regional Leaders in AI Adoption": """
        SELECT Region,
               ROUND(AVG("Adoption_Rate_%"), 2) AS avg_adoption_rate
        FROM   ai_adoption
        GROUP  BY Region
        ORDER  BY avg_adoption_rate DESC;
    """,
}

for title, query in queries.items():
    print(f"\n{title}")
    print("-" * 50)
    result = pd.read_sql_query(query, conn)
    print(result.to_string(index=False))

conn.close()
print("\n✅ SQL analysis complete.")
