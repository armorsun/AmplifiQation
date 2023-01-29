import os
import psycopg2
from flask import Flask, render_template
import randomizer
import covalent as ct
import pandas as pds
import Hamiltonian
from sqlalchemy import create_engine

app = Flask(__name__)

def get_db_connection():
    conn = psycopg2.connect(host='db',
                            database='iQuHack',
                            user=os.environ['DB_USERNAME'],
                            password=os.environ['DB_PASSWORD'])
    return conn

def get_pandas_db():
    alchemyEngine  = create_engine("postgresql+psycopg2://postgres:postgres@db/iQuHack", pool_recycle=3600);
    conn = alchemyEngine.connect();
    
    return conn

@app.route('/')
def index():
    return "AmplifiQation"

@app.route('/random')
@ct.electron
def random():
    # 0 for local simulator, 1 for IBM sim, 2 for QC
    token = os.environ["IBM_QUANTUM_TOKEN"]
    random_numbers = randomizer.RNG(1, token)
    random_number = random_numbers.randomizer_circuit(2)
    print(random_number)
    return str(random_number)

@app.route('/pandas')
@ct.lattice
def pandas():
    conn = get_pandas_db()
    dataFrame = pds.read_sql("select * from locations", conn);
    hamiltonian = Hamiltonian.Hamiltonian(dataFrame);
    distance_matrix = hamiltonian.get_distance_matrix(4)
    print(distance_matrix)
    conn.close();
    return "pandas"
    
