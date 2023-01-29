import os
import psycopg2
from flask import Flask, render_template
import randomizer
import covalent as ct
import pandas as pds

app = Flask(__name__)

def get_db_connection():
    conn = psycopg2.connect(host='db',
                            database='iQuHack',
                            user=os.environ['DB_USERNAME'],
                            password=os.environ['DB_PASSWORD'])
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM ;')
    books = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('index.html', books=books)

@app.route('/random')
@ct.electron
def random():
    # 0 for local simulator, 1 for IBM sim, 2 for QC
    token = os.environ["IBM_QUANTUM_TOKEN"]
    random_numbers = randomizer.RNG(token, 1)
    random_number = random_numbers.randomizer_circuit(2)
    print(random_number)
    return str(random_number)

@app.route('/pandas')
def pandas():
    conn = get_db_connection()
    dataFrame = pds.read_sql("select * from \"locations\"", conn);
    pds.set_option('display.expand_frame_repr', False);
    print(dataFrame);
    conn.close();
    return "pandas"
    
