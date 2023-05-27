import requests
from bs4 import BeautifulSoup
import sqlite3

def salvar_resultados_mega_sena():
    # Conectar com o banco de dados
    conn = sqlite3.connect('megasena.db')
    cursor = conn.cursor()

    # Criar tabela de resultados, caso ela ainda não exista
    cursor.execute('''CREATE TABLE IF NOT EXISTS resultados
                      (concurso INTEGER PRIMARY KEY, data_sorteio TEXT, bola1 INTEGER, bola2 INTEGER, bola3 INTEGER,
                       bola4 INTEGER, bola5 INTEGER, bola6 INTEGER, acumulado BOOLEAN, valor_acumulado REAL,
                       acumulado_especial REAL)''')

    # Obter os resultados dos últimos 2583 concursos
    for concurso in range(1, 2584):
        print(f'Salvando resultado do concurso {concurso}...')
        url = f'https://www.lotterycorner.com/results/br/mega-sena/{concurso}'
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Verificar se o resultado existe
        if not soup.select_one('.nav-anchor'):
            continue

        # Extrair informações do resultado
        resultado = {}
        resultado['concurso'] = concurso
        resultado['data_sorteio'] = soup.select_one('.nav-anchor').text.split()[-2][1:-1]
        resultado['bola1'] = int(soup.select_one('.result-number li:nth-of-type(1)').text)
        resultado['bola2'] = int(soup.select_one('.result-number li:nth-of-type(2)').text)
        resultado['bola3'] = int(soup.select_one('.result-number li:nth-of-type(3)').text)
        resultado['bola4'] = int(soup.select_one('.result-number li:nth-of-type(4)').text)
        resultado['bola5'] = int(soup.select_one('.result-number li:nth-of-type(5)').text)
        resultado['bola6'] = int(soup.select_one('.result-number li:nth-of-type(6)').text)
        resultado['acumulado'] = soup.select_one('.resultado-loteria h3.epsilon').text == 'Acumulou!'
        acumulados = soup.select('.totals p.ng-binding')
        acumulados_valores = soup.select('.totals p.value.ng-binding')
        for i, acumulado in enumerate(acumulados):
            if 'Acumulado próximo' in acumulado.text:
                resultado['valor_acumulado'] = float(acumulados_valores[i].text[3:].replace(',', '.'))
            elif 'Acumulado para Sorteio Especial' in acumulado.text:
                resultado['acumulado_especial'] = float(acumulados_valores[i].text[3:].replace(',', '.'))

        # Salvar resultado no banco de dados
        cursor.execute('INSERT INTO resultados VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                       (resultado['concurso'], resultado['data_sorteio'], resultado['bola1'], resultado['bola2'],
                        resultado['bola3'], resultado['bola4'], resultado['bola5'], resultado['bola6'],
                        resultado['acumulado'], resultado.get('valor_acumulado'), resultado.get('acumulado_especial')))
        conn.commit()

    # Fechar a conexão com o banco de dados
    cursor.close()
    conn.close()

salvar_resultados_mega_sena()
