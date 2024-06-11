# Sistema de Informações de Companhias Abertas

## Descrição do Projeto
Este projeto consiste na criação de um sistema em Python para persistir informações sobre companhias abertas em um banco de dados SQL e permitir a consulta desses dados posteriormente. As informações podem variar de uma data para outra, como o nome da empresa (DENOM_SOCIAL) e a situação (SIT). O usuário poderá acessar os dados de uma determinada data ou CNPJ.

## Fonte de Dados
As informações sobre as companhias são públicas e podem ser baixadas no seguinte link: [dados.gov - Cias Abertas](https://dados.gov.br/dados/conjuntos-dados/cias-abertas-informao-cadastral)

# Instruções
<details>
  <summary><strong>⚠ Pré-requisitos</strong></summary><br />

  Antes de executar este projeto, certifique-se de ter o seguinte instalado em seu sistema:

  * [Python (versão 3.x)](https://www.python.org/downloads/)
  * [pip (Gerenciador de pacotes Python)](https://pip.pypa.io/en/stable/installation/)

</details>

<details>
  <summary><strong>🛠 Preparando a aplicação para uso</strong></summary><br />
  Criar e ativar o ambiente virtual para instalar as depências do projeto.

  1. Clone o repositório
  ```bash
  git clone git@github.com:nickolasvm/sparta-python-project.git
  ```

  2. Entre na pasta do repositório que você acabou de clonar
  ```bash
  cd sparta-python-project
  ```

  3. Crie o ambiente virtual para o projeto
  ```bash
  python3 -m venv .venv && source .venv/bin/activate
  ```
  
  4. Instale as dependências
  ```bash
  python3 -m pip install -r requirements.txt
  ```
</details>
  
<details>
  <summary><strong>🏃🏾 Executando a aplicação</strong></summary><br />

  1. Inicie a aplicação com o script abaixo
  
  ```bash
  python main.py
  ```
  
  2. Ao iniciar, será criado uma pasta data/input. Baixe o arquivo de dados neste [link](https://dados.gov.br/dados/conjuntos-dados/cias-abertas-informao-cadastral) e mova-o para a pasta criada
  ```bash
  project_root/
  ├── main.py
  ├── data/
  │   ├── database/
  │   └── input/
  │       ├── (Inclua o arquivo .csv aqui)
  ...
  ```

  3. Siga as instruções na tela para importar o arquivo no banco de dados e realizar consultas.
</details>

# Sobre o projeto

## Pacotes e bibliotecas

* SQLite: Banco de dados SQLite, pois é uma solução leve e embutida, adequada para projetos de pequeno porte.
* pandas: Os arquivos .csv são importados para o banco de dados utilizando a biblioteca pandas, devido à sua eficiência no tratamento de dados.
* PrettyTable: utilizado para imprimir tabelas em formato ASCII visualmente atrativas. (American Standard Code for Information Interchange).
* flake8: Linter para manter o código limpo, legível e padronizado.

## Tomada de decisões

* User interface: Optou-se por uma interface de linha de comando (CLI) simples, permitindo ao usuário interagir com o sistema de forma intuitiva.
  * A utilização de uma CLI sobre uma API foi pensada para manter a simplicidade do projeto.
* ORM: Optou-se por não utilizar ORM neste projeto para manter simplicidade e controle total sobre as consultas SQL, otimizando desempenho e adaptando-se às necessidades específicas do banco de dados.

## Implementações Faltantes

* Testes unitários | integração: No momento, este projeto carece de testes implementados. Podemos incorporar testes unitários utilizando a bibliotecas como unittest ou pytest.

