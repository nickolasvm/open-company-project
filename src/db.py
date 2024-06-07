import sqlite3
import csv
from prettytable import from_db_cursor
from datetime import datetime


def create_connection(db_file):
    conn = sqlite3.connect(db_file)
    return conn


def initialize_database(conn):
    create_table_query = '''
    CREATE TABLE IF NOT EXISTS cias_abertas (
        id INTEGER PRIMARY KEY,
        cnpj_cia TEXT,
        denom_social TEXT,
        sit TEXT,
        created_at DATE NOT NULL
    );
    '''
    cursor = conn.cursor()
    try:
        cursor.execute(create_table_query)
    except sqlite3.OperationalError as err:
        print(f'''
              Aconteceu um erro durante a criação da tabela
              de companhias abertas no banco: {err}''')
    conn.commit()


def insert_data_from_csv(conn, csv_file):
    cursor = conn.cursor()

    with open(csv_file, mode='r', newline='', encoding='iso-8859-1') as file:
        reader = csv.reader(file, delimiter=';')

        header = next(reader)

        # Find columns indexes
        cnpj_cia_i = header.index("CNPJ_CIA")
        denom_social_i = header.index("DENOM_SOCIAL")
        sit_i = header.index("SIT")

        for row in reader:
            cnpj_cia = row[cnpj_cia_i]
            denom_social = row[denom_social_i]
            sit = row[sit_i]
            created_at = datetime.now().strftime('%Y-%m-%d')
            insert_query = '''
            INSERT INTO cias_abertas
            (cnpj_cia, denom_social, sit, created_at)
            VALUES (?, ?, ?, ?)
            '''
            cursor.execute(
                insert_query,
                (cnpj_cia, denom_social, sit, created_at))

    conn.commit()


def fetch_by_date(conn, date_str):
    # Convert date string to object
    date_obj = datetime.strptime(date_str, '%d/%m/%Y')
    formatted_date = date_obj.strftime('%Y-%m-%d')

    cursor = conn.cursor()
    select_query = '''
    SELECT id, cnpj_cia, denom_social, sit
    FROM cias_abertas
    WHERE DATE(created_at) = ?
    '''
    cursor.execute(select_query, (formatted_date,))

    table = from_db_cursor(cursor)
    table.align['denom_social'] = 'l'
    print(table)
