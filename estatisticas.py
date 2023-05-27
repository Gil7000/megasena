import datetime
import sqlite3

def conectar_banco():
    conn = sqlite3.connect('megasena.db')
    cursor = conn.cursor()
    return conn, cursor

def desconectar_banco(conn, cursor):
    cursor.close()
    conn.close()


def criar_tabela_dezenas(cursor):
    # Criar tabela de dezenas, caso ela ainda não exista
    cursor.execute('''CREATE TABLE IF NOT EXISTS dezenas
                      (numero INTEGER PRIMARY KEY, ultimo_sorteio INTEGER, data_sorteio TEXT)''')

def atualizar_tabela_dezenas(cursor):
    # Busca as dezenas presentes na tabela de dezenas
    cursor.execute('SELECT numero FROM dezenas')
    dezenas = [d[0] for d in cursor.fetchall()]

    # Busca a bola mais recente em cada posição
    cursor.execute('SELECT bola1, bola2, bola3, bola4, bola5, bola6 FROM resultados ORDER BY concurso DESC LIMIT 1')
    ultima_bola = cursor.fetchone()

    # Atualiza a tabela de dezenas com os valores das bolas mais recentes
    for bola in ultima_bola:
        if bola in dezenas:
            cursor.execute(f"UPDATE dezenas SET ultimo_sorteio = '{ultima_bola}', data_sorteio = '{str(datetime.datetime.now().date())}' WHERE numero = {bola}")
        else:
            cursor.execute(f"INSERT INTO dezenas (numero, ultimo_sorteio, data_sorteio) VALUES ({bola}, '{ultima_data}', '{str(datetime.datetime.now().date())}')")

import datetime
import sqlite3

def dezenas_nao_sorteadas_ha_mais_tempo(limit=10):
    conn = sqlite3.connect('megasena.db')
    cursor = conn.cursor()

    # Obter a data do último sorteio
    cursor.execute('SELECT data_sorteio FROM resultados ORDER BY concurso DESC LIMIT 1')
    ultima_data_sorteio = datetime.datetime.strptime(cursor.fetchone()[0], '%d/%m/%Y').date()

    # Obter as dezenas sorteadas e calcular a diferença de dias em relação à data atual
    cursor.execute('SELECT bola1, bola2, bola3, bola4, bola5, bola6 FROM resultados ORDER BY concurso DESC LIMIT 1')
    dezenas_sorteadas = set(cursor.fetchone())
    dezenas_nao_sorteadas = set(range(1, 61)) - dezenas_sorteadas
    dezenas_nao_sorteadas_ha_mais_tempo = []
    for dezena in dezenas_nao_sorteadas:
        cursor.execute(f'SELECT data_sorteio FROM resultados WHERE bola1 = {dezena} OR bola2 = {dezena} OR bola3 = {dezena} OR bola4 = {dezena} OR bola5 = {dezena} OR bola6 = {dezena} ORDER BY concurso DESC LIMIT 1')
        ultima_data_sorteio_dezena = datetime.datetime.strptime(cursor.fetchone()[0], '%d/%m/%Y').date()
        dias_desde_ultimo_sorteio = (ultima_data_sorteio - ultima_data_sorteio_dezena).days
        dezenas_nao_sorteadas_ha_mais_tempo.append((dezena, dias_desde_ultimo_sorteio, ultima_data_sorteio_dezena))

    # Ordenar pelo tempo desde o último sorteio e limitar a quantidade de resultados
    dezenas_nao_sorteadas_ha_mais_tempo.sort(key=lambda x: x[1], reverse=True)
    resultado = dezenas_nao_sorteadas_ha_mais_tempo[:limit]

    conn.close()
    return resultado


def dezenas_mais_sorteadas(limit=10):
    conn, cursor = conectar_banco()
    cursor.execute(f'''
        SELECT bola, COUNT(*) as count
        FROM (SELECT bola1 as bola FROM resultados
              UNION ALL SELECT bola2 as bola FROM resultados
              UNION ALL SELECT bola3 as bola FROM resultados
              UNION ALL SELECT bola4 as bola FROM resultados
              UNION ALL SELECT bola5 as bola FROM resultados
              UNION ALL SELECT bola6 as bola FROM resultados)
        GROUP BY bola
        ORDER BY count DESC
        LIMIT {limit}
    ''')
    resultado = cursor.fetchall()
    desconectar_banco(conn, cursor)
    return resultado

def dezenas_menos_sorteadas(limit=10):
    conn, cursor = conectar_banco()
    cursor.execute(f'''
        SELECT bola, COUNT(*) as count
        FROM (SELECT bola1 as bola FROM resultados
              UNION ALL SELECT bola2 as bola FROM resultados
              UNION ALL SELECT bola3 as bola FROM resultados
              UNION ALL SELECT bola4 as bola FROM resultados
              UNION ALL SELECT bola5 as bola FROM resultados
              UNION ALL SELECT bola6 as bola FROM resultados)
        GROUP BY bola
        ORDER BY count ASC
        LIMIT {limit}
    ''')
    resultado = cursor.fetchall()
    desconectar_banco(conn, cursor)
    return resultado

def combinacoes_4_mais_repetidas(limit=10):
    conn, cursor = conectar_banco()
    cursor.execute(f'''
        SELECT dezenas, COUNT(*) as count
        FROM (SELECT DISTINCT resultado1.bola1 || ',' || resultado1.bola2 || ',' || resultado1.bola3 || ',' || resultado1.bola4 as dezenas
              FROM resultados as resultado1
              JOIN resultados as resultado2
              ON resultado1.concurso != resultado2.concurso
              WHERE resultado1.bola1 IN (resultado2.bola1, resultado2.bola2, resultado2.bola3, resultado2.bola4, resultado2.bola5, resultado2.bola6)
                AND resultado1.bola2 IN (resultado2.bola1, resultado2.bola2, resultado2.bola3, resultado2.bola4, resultado2.bola5, resultado2.bola6)
                AND resultado1.bola3 IN (resultado2.bola1, resultado2.bola2, resultado2.bola3, resultado2.bola4, resultado2.bola5, resultado2.bola6)
                AND resultado1.bola4 IN (resultado2.bola1, resultado2.bola2, resultado2.bola3, resultado2.bola4, resultado2.bola5, resultado2.bola6))
        GROUP BY dezenas
        ORDER BY count DESC
        LIMIT {limit}
    ''')
    resultado = cursor.fetchall()
    desconectar_banco(conn, cursor)
    return resultado

def combinacoes_5_mais_repetidas(limit=10):
    conn, cursor = conectar_banco()
    cursor.execute(f'''
        SELECT dezenas, COUNT(*) as count
        FROM (SELECT DISTINCT resultado1.bola1 || ',' || resultado1.bola2 || ',' || resultado1.bola3 || ',' || resultado1.bola4 || ',' || resultado1.bola5 as dezenas
              FROM resultados as resultado1
              JOIN resultados as resultado2
              ON resultado1.concurso != resultado2.concurso
              WHERE resultado1.bola1 IN (resultado2.bola1, resultado2.bola2, resultado2.bola3, resultado2.bola4, resultado2.bola5, resultado2.bola6)
                AND resultado1.bola2 IN (resultado2.bola1, resultado2.bola2, resultado2.bola3, resultado2.bola4, resultado2.bola5, resultado2.bola6)
                AND resultado1.bola3 IN (resultado2.bola1, resultado2.bola2, resultado2.bola3, resultado2.bola4, resultado2.bola5, resultado2.bola6)
                AND resultado1.bola4 IN (resultado2.bola1, resultado2.bola2, resultado2.bola3, resultado2.bola4, resultado2.bola5, resultado2.bola6)
                AND resultado1.bola5 IN (resultado2.bola1, resultado2.bola2, resultado2.bola3, resultado2.bola4, resultado2.bola5, resultado2.bola6))
        GROUP BY dezenas
        ORDER BY count DESC
        LIMIT {limit}
    ''')
    resultado = cursor.fetchall()
    desconectar_banco(conn, cursor)
    return resultado

def combinacoes_6_mais_repetidas(limit=10):
    conn, cursor = conectar_banco()
    cursor.execute(f'''
        SELECT dezenas, COUNT(*) as count
        FROM (SELECT DISTINCT resultado1.bola1 || ',' || resultado1.bola2 || ',' || resultado1.bola3 || ',' || resultado1.bola4 || ',' || resultado1.bola5 || ',' || resultado1.bola6 as dezenas
              FROM resultados as resultado1
              JOIN resultados as resultado2
              ON resultado1.concurso != resultado2.concurso
              WHERE resultado1.bola1 IN (resultado2.bola1, resultado2.bola2, resultado2.bola3, resultado2.bola4, resultado2.bola5, resultado2.bola6)
                AND resultado1.bola2 IN (resultado2.bola1, resultado2.bola2, resultado2.bola3, resultado2.bola4, resultado2.bola5, resultado2.bola6)
                AND resultado1.bola3 IN (resultado2.bola1, resultado2.bola2, resultado2.bola3, resultado2.bola4, resultado2.bola5, resultado2.bola6)
                AND resultado1.bola4 IN (resultado2.bola1, resultado2.bola2, resultado2.bola3, resultado2.bola4, resultado2.bola5, resultado2.bola6)
                AND resultado1.bola5 IN (resultado2.bola1, resultado2.bola2, resultado2.bola3, resultado2.bola4, resultado2.bola5, resultado2.bola6)
                AND resultado1.bola6 IN (resultado2.bola1, resultado2.bola2, resultado2.bola3, resultado2.bola4, resultado2.bola5, resultado2.bola6))
        GROUP BY dezenas
        ORDER BY count DESC
        LIMIT {limit}
    ''')
    resultado = cursor.fetchall()
    desconectar_banco(conn, cursor)
    return resultado

def pares_impares():
    conn, cursor = conectar_banco()
    cursor.execute('''
        SELECT
            SUM(CASE WHEN bola % 2 = 0 THEN 1 ELSE 0 END) as pares,
            SUM(CASE WHEN bola % 2 = 1 THEN 1 ELSE 0 END) as impares
        FROM (SELECT bola1 as bola FROM resultados
              UNION ALL SELECT bola2 as bola FROM resultados
              UNION ALL SELECT bola3 as bola FROM resultados
              UNION ALL SELECT bola4 as bola FROM resultados
              UNION ALL SELECT bola5 as bola FROM resultados
              UNION ALL SELECT bola6 as bola FROM resultados)
    ''')
    resultado = cursor.fetchone()
    desconectar_banco(conn, cursor)
    return resultado


def soma_numeros_mais_sorteados(limit=10):
    conn, cursor = conectar_banco()
    cursor.execute(f'''
        SELECT soma, COUNT(*) as count
        FROM (SELECT SUM(bola1 + bola2 + bola3 + bola4 + bola5 + bola6) as soma
              FROM resultados
              GROUP BY concurso)
        GROUP BY soma
        ORDER BY count DESC, soma
        LIMIT {limit}
    ''')
    resultado = cursor.fetchall()
    desconectar_banco(conn, cursor)
    return resultado
