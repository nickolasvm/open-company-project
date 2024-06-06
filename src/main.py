import db


def import_csv_to_database(conn):
    try:
        csv_file = 'data/input/cad_cia_aberta.csv'
        db.insert_data_from_csv(conn, csv_file)
        print('\nArquivo importado com sucesso!')
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
