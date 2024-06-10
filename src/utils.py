def paginate_table(table, page_size=100):
    total_rows = len(table.rows)

    # Mostra tabela inteira caso haja menos linhas que page_size
    if (total_rows < page_size):
        print(table)
        return

    #  Incluindo page_size - 1 garante que a divisão vai arredondar para o número mais próximo
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
    # Quebra a string em segmentos
    segments = [cnpj_str[:2], cnpj_str[2:5], cnpj_str[5:8], cnpj_str[8:12], cnpj_str[12:]]

    # Junta os segmentos
    formatted_cnpj = '{}.{}.{}/{}-{}'.format(*segments)

    return formatted_cnpj
