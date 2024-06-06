import sqlite3
import csv
from datetime import datetime


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
        created_at DATE NOT NULL
    );
    '''
    cursor = conn.cursor()
    cursor.execute(create_table_query)
    conn.commit()


def insert_data_from_csv(conn, csv_file):
    cursor = conn.cursor()

    with open(csv_file, mode='r', newline='') as file:
        reader = csv.reader(file)

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
            VALUES (?, ?, ?)
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
    select_query = "SELECT * FROM cias_abertas WHERE DATE(created_at) = ?"
    cursor.execute(select_query, (formatted_date,))
    rows = cursor.fetchall()
    for row in rows:
        print(row)
