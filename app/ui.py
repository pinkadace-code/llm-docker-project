import os
import logging
from flask import Flask, request, jsonify, render_template
from groq import Groq
import mysql.connector

# Logging iestatīšana
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
log = logging.getLogger(__name__)

app = Flask(__name__)

def connect_db():
    return mysql.connector.connect(
        host=os.environ.get("DB_HOST"),
        port=int(os.environ.get("DB_PORT", 3306)),
        user=os.environ.get("DB_USER"),
        password=os.environ.get("DB_PASSWORD"),
        database=os.environ.get("DB_NAME")
    )

def get_db_context(conn):
    cursor = conn.cursor()
    context = ""
    cursor.execute("SHOW TABLES")
    tables = cursor.fetchall()
    for (table,) in tables:
        context += f"\nTabula: {table}\n"
        cursor.execute(f"DESCRIBE {table}")
        for col in cursor.fetchall():
            context += f"  - {col[0]} ({col[1]})\n"
    return context

@app.route('/')
def index():
    log.info("Lietotājs atvēra galveno lapu")
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    question = request.json.get('question')
    log.info(f"Saņemts jautājums: {question}")
    
    try:
        conn = connect_db()
        context = get_db_context(conn)
        
        client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
        
        prompt = f"""Datubāze satur šādas tabulas:
{context}

Lietotāja jautājums: {question}

Uzraksti SQL vaicājumu kas atbild uz šo jautājumu, un paskaidro ko tas darīs."""
        
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}]
        )
        
        answer = response.choices[0].message.content
        log.info("Atbilde veiksmīgi ģenerēta")
        conn.close()
        return jsonify({"answer": answer})
    
    except Exception as e:
        log.error(f"Kļūda: {str(e)}")
        return jsonify({"answer": f"Kļūda: {str(e)}"})

if __name__ == '__main__':
    log.info("=== UI serveris startē ===")
    app.run(host='0.0.0.0', port=5000, debug=True)