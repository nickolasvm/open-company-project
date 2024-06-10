import sqlite3
import pandas as pd
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
    df = pd.read_csv(csv_file, delimiter=';', encoding='iso-8859-1')
    df = df[['CNPJ_CIA', 'DENOM_SOCIAL', 'SIT']]
    # Delete duplicates
    df = df.drop_duplicates(subset=['CNPJ_CIA', 'DENOM_SOCIAL', 'SIT'])
    df['created_at'] = datetime.now().strftime('%Y-%m-%d')

    cursor = conn.cursor()
    insert_query = '''
    INSERT INTO cias_abertas
    (cnpj_cia, denom_social, sit, created_at)
    VALUES (?, ?, ?, ?)
    '''

    for row in df.iterrows():
        try:
            cursor.execute(insert_query, (row['CNPJ_CIA'], row['DENOM_SOCIAL'], row['SIT'], row['created_at']))
        except sqlite3.OperationalError as err:
            print(f'Aconteceu um erro durante a inserção de dados no banco: {err}')

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
    try:
        cursor.execute(select_query, (formatted_date,))
    except sqlite3.OperationalError as err:
        print(f'Ocorreu um erro durante a query por data no banco: {err}')

    table = from_db_cursor(cursor)
    table.align['denom_social'] = 'l'

    if len(table.rows) < 1:
        print('\nNão existe dados para a data informada.')
    else:
        paginate_table(table)


def fetch_by_cnpj(conn, cnpj_str):
    # Convert CNPJ to format XX.XXX.XXX/XXXX-XX
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


def paginate_table(table, page_size=100):
    total_rows = len(table.rows)

    # Don't need to paginate if there is less rows than page size
    if (total_rows < page_size):
        print(table)
        return

    #  Adding page_size - 1 ensures that the division will round up to the nearest integer
    num_pages = (total_rows + page_size - 1) // page_size
    current_page = 1

    while True:
        print('\n')
        start_index = (current_page - 1) * page_size
        end_index = min(total_rows, current_page * page_size)

        print(table.get_string(start=start_index, end=end_index))

        print(f'\nPágina {current_page}/{num_pages}')

        user_input = input('Pressione Enter para continuar à próxima página (ou "q" para sair): ')
        if user_input.lower() == 'q':
            break
        current_page += 1
        if current_page > num_pages:
            print('Fim dos dados.')
            break


def format_cnpj(cnpj_str):
    # Split the string into segments
    segments = [cnpj_str[:2], cnpj_str[2:5], cnpj_str[5:8], cnpj_str[8:12], cnpj_str[12:]]

    # Join segments
    formatted_cnpj = '{}.{}.{}/{}-{}'.format(*segments)

    return formatted_cnpj
