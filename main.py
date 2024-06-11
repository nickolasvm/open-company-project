import src.db as db
import os

DB_PATH = 'data/db'
CSV_PATH = 'data/input'
CSV_FILE_PATH = f'{CSV_PATH}/cad_cia_aberta.csv'


def create_directory():
    # Cria diretório caso não exista
    if not os.path.exists(DB_PATH):
        os.makedirs(DB_PATH)

    if not os.path.exists(CSV_PATH):
        os.makedirs(CSV_PATH)


def delete_csv():
    os.remove(CSV_FILE_PATH)
    print('\nArquivo excluído com sucesso!')


def import_csv_to_database(conn):
    try:
        #  Importa arquivo
        db.insert_data_from_csv(conn, CSV_FILE_PATH)
        print('\nArquivo importado com sucesso!')

        #  Deleta arquivo após importação
        print('\nDeseja excluir o arquivo? (Recomendado) S/N')
        choice = input('')

        while choice.lower() not in ['s', 'n']:
            print('\nEscolha inválida. Tente novamente.')
            print('\nDeseja excluir o arquivo? (Recomendado) S/N')
            choice = input('')

        if choice.lower() == 's':
            delete_csv()

    except FileNotFoundError:
        print('''
        Arquivo .csv não encontrado!
        Certifique-se de que o arquivo exista na pasta "data/input"
        ''')


def fetch_results_by_date(conn, filter):
    try:
        date_str = input('\nInsira uma data para pesquisar (DD/MM/YYYY): ')
        if filter == '1':
            db.fetch_by_date(conn, date_str, 'ATIVO')
        elif filter == '2':
            db.fetch_by_date(conn, date_str, 'CANCELADA')
        else:
            db.fetch_by_date(conn, date_str)
    except ValueError:
        print('\nData inválida!')


def fetch_results_by_cnpj(conn):
    cnpj_str = input('\nDigite o CNPJ a ser pesquisado (apenas números): ')
    if not cnpj_str.isdigit() or len(cnpj_str) != 14:
        print('\nCNPJ inválido!')
    else:
        db.fetch_by_cnpj(conn, cnpj_str)


def main():
    # Checa existência das pastas
    create_directory()

    # Cria conexão com o banco
    conn = db.create_connection(f'{DB_PATH}/database.db')

    # Inicializa o banco
    db.initialize_database(conn)

    while True:
        print('\nSelecione uma das opções:\n')
        print('1. Importar arquivo .csv para o banco de dados')
        print('2. Pesquisar empresas por data')
        print('3. Pesquisar empresa por CNPJ')
        print('4. Sair')

        match input(''):
            case '1':
                import_csv_to_database(conn)
            case '2':
                print('\nFiltrar por:\n')
                print('1. Empresas ativas')
                print('2. Empresas canceladas')
                print('3. Todas as empresas')

                filter = input('')
                while filter not in ['1', '2', '3']:
                    print('\nEscolha inválida. Tente novamente.')
                    filter = input('')

                fetch_results_by_date(conn, filter)
            case '3':
                fetch_results_by_cnpj(conn)
            case '4':
                break
            case _:
                print('\nEscolha inválida. Tente novamente.')

    # Fecha conexão
    conn.close()


if __name__ == '__main__':
    main()
