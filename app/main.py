import os
import logging
from groq import Groq
import mysql.connector
import pandas as pd

# Logging iestatīšana
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
log = logging.getLogger(__name__)

# Savienojums ar datubāzi
def connect_db():
    log.info("Savienojas ar datubāzi...")
    conn = mysql.connector.connect(
        host=os.environ.get("DB_HOST"),
        port=int(os.environ.get("DB_PORT", 3306)),
        user=os.environ.get("DB_USER"),
        password=os.environ.get("DB_PASSWORD"),
        database=os.environ.get("DB_NAME")
    )
    log.info("Savienojums veiksmīgs!")
    return conn

# Konteksta ģenerēšana
def get_db_context(conn):
    log.info("Iegūst datubāzes struktūru...")
    cursor = conn.cursor()
    context = ""
    cursor.execute("SHOW TABLES")
    tables = cursor.fetchall()
    for (table,) in tables:
        context += f"\nTabula: {table}\n"
        cursor.execute(f"DESCRIBE {table}")
        for col in cursor.fetchall():
            context += f"  - {col[0]} ({col[1]})\n"
    log.info("Konteksts iegūts!")
    return context

# Groq AI pieslēgšana
def ask_groq(client, prompt):
    log.info("Sūta vaicājumu Groq AI...")
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

def main():
    log.info("=== LLM Context Generator sāk darbu ===")
    
    # Datubāze
    conn = connect_db()
    context = get_db_context(conn)
    print("\nDatubāzes konteksts:")
    print(context)
    
    # Groq klients
    client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
    
    # SQL ģenerēšana
    prompt = f"""Datubāze satur šādas tabulas:
{context}

Uzraksti SQL vaicājumu kas parāda kopējo maksājumu summu pa valūtām."""
    
    sql = ask_groq(client, prompt)
    log.info("SQL vaicājums ģenerēts!")
    print("\nĢenerētais SQL:")
    print(sql)
    
    conn.close()
    log.info("=== Darbs pabeigts ===")

if __name__ == "__main__":
    main()