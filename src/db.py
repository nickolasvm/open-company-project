import sqlite3


def create_connection(db_file):
    conn = sqlite3.connect(db_file)
    return conn


def initialize_database(conn):
    create_table_query = '''
    CREATE TABLE IF NOT EXISTS cias_abertas (
        id INTEGER PRIMARY KEY,
        cnpj_cia TEXT NOT NULL,
        denom_social TEXT NOT NULL,
        sit TEXT NOT NULL,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    );
    '''
    cursor = conn.cursor()
    cursor.execute(create_table_query)
    conn.commit()
