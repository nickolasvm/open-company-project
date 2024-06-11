import sqlite3
import pandas as pd
from prettytable import from_db_cursor
from datetime import datetime
from src.utils import paginate_table, format_cnpj


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
    df = pd.read_csv(csv_file, delimiter=';', encoding='iso-8859-1')
    df = df[['CNPJ_CIA', 'DENOM_SOCIAL', 'SIT']]
    # Deleta duplicados
    df = df.drop_duplicates(subset=['CNPJ_CIA', 'DENOM_SOCIAL', 'SIT'])
    df['created_at'] = datetime.now().strftime('%Y-%m-%d')

    cursor = conn.cursor()
    insert_query = '''
    INSERT INTO cias_abertas
    (cnpj_cia, denom_social, sit, created_at)
    VALUES (?, ?, ?, ?)
    '''

    for _, row in df.iterrows():
        try:
            cursor.execute(insert_query, (row['CNPJ_CIA'], row['DENOM_SOCIAL'], row['SIT'], row['created_at']))
        except sqlite3.OperationalError as err:
            print(f'Aconteceu um erro durante a inserção de dados no banco: {err}')

    conn.commit()


def fetch_by_date(conn, date_str, sit_filter=None):
    # Converte a string de data em objeto
    date_obj = datetime.strptime(date_str, '%d/%m/%Y')
    formatted_date = date_obj.strftime('%Y-%m-%d')

    cursor = conn.cursor()
    select_query = '''
    SELECT id, cnpj_cia, denom_social, sit
    FROM cias_abertas
    WHERE DATE(created_at) = ?
    '''

    # Adiciona filtro
    if sit_filter:
        select_query += ' AND sit = ?'
        query_params = (formatted_date, sit_filter)
    else:
        query_params = (formatted_date,)

    try:
        cursor.execute(select_query, query_params)
    except sqlite3.OperationalError as err:
        print(f'Ocorreu um erro durante a query por data no banco: {err}')

    table = from_db_cursor(cursor)
    table.align['denom_social'] = 'l'

    if len(table.rows) < 1:
        print('\nNão existe dados para a data informada.')
    else:
        paginate_table(table)


def fetch_by_cnpj(conn, cnpj_str):
    # Converte CNPJ para formato XX.XXX.XXX/XXXX-XX
    cnpj = format_cnpj(cnpj_str)

    cursor = conn.cursor()
    select_query = '''
    SELECT cnpj_cia, denom_social, sit, created_at
    FROM cias_abertas
    WHERE cnpj_cia = ?
    '''
    try:
        cursor.execute(select_query, (cnpj,))
    except sqlite3.OperationalError as err:
        print(f'Ocorreu um erro durante a query por data no banco: {err}')

    table = from_db_cursor(cursor)
    table.align['denom_social'] = 'l'

    if len(table.rows) < 1:
        print('\nNão existe dados para este CNPJ.')
    else:
        paginate_table(table)
