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
        cnpj_cia_i = header.index('CNPJ_CIA')
        denom_social_i = header.index('DENOM_SOCIAL')
        sit_i = header.index('SIT')

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
            try:
                cursor.execute(
                    insert_query,
                    (cnpj_cia, denom_social, sit, created_at))
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


def paginate_table(table, page_size=100):
    total_rows = len(table.rows)
    #  Adding page_size - 1 ensures that the division will round up to the nearest integer
    num_pages = (total_rows + page_size - 1) // page_size
    print(num_pages)
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
