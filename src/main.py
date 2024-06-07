import db
import os

CSV_FILE_PATH = 'data/input/cad_cia_aberta.csv'


def delete_csv():
    os.remove(CSV_FILE_PATH)
    print('\nArquivo excluído com sucesso!')


def import_csv_to_database(conn):
    try:
        #  Import file
        db.insert_data_from_csv(conn, CSV_FILE_PATH)
        print('\nArquivo importado com sucesso!')

        #  Delete file after importing it
        print('\nDeseja excluir o arquivo? (Recomendado) S/N')
        choice = input('')

        while choice.lower() not in ["s", "n"]:
            print('\nEscolha inválida. Tente novamente.')
            print('\nDeseja excluir o arquivo? (Recomendado) S/N')
            choice = input('')

        if choice.lower() == 's':
            delete_csv()

    except FileNotFoundError:
        print('''
        Arquivo .csv não encontrado!
        Certifique-se que o arquivo existe na pasta "data/input"
        ''')


def fetch_results_by_date(conn):
    try:
        date_str = input('\nInsira uma data para pesquisar (DD/MM/YYYY): ')
        db.fetch_by_date(conn, date_str)
    except ValueError:
        print("\nData inválida!")


def main():
    # Create connection
    conn = db.create_connection('data/db/database.db')

    #  Initialize database
    db.initialize_database(conn)

    while True:
        print('\nSelecione uma das opções:\n')
        print('1. Importar arquivo .csv para o banco de dados')
        print('2. Pesquisar cias por data')
        print('3. Sair')

        choice = input('')

        if choice == '1':
            import_csv_to_database(conn)
        elif choice == '2':
            fetch_results_by_date(conn)
        elif choice == '3':
            break
        else:
            print('\nEscolha inválida. Tente novamente.')

    # Close connection
    conn.close()


if __name__ == '__main__':
    main()
