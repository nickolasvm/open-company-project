import db


def import_csv_to_database(conn):
    csv_file = 'data/input/cad_cia_aberta.csv'
    db.insert_data_from_csv(conn, csv_file)
    print('Arquivo importado com sucesso!')


def fetch_results_by_date(conn):
    date_str = input('Insira uma data para pesquisar (DD/MM/YYYY): ')
    db.fetch_by_date(conn, date_str)


def main():
    # Create connection
    conn = db.create_connection('data/db/database.db')

    #  Initialize database
    db.initialize_database(conn)

    while True:
        print('\nOpções:')
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
            print('Escolha inválida. Tente novamente.')

    # Close connection
    conn.close()


if __name__ == '__main__':
    main()
