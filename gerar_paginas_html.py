import sqlite3
from jinja2 import Environment, FileSystemLoader

def conectar_banco():
    conn = sqlite3.connect('megasena.db')
    cursor = conn.cursor()
    return conn, cursor

def desconectar_banco(conn, cursor):
    cursor.close()
    conn.close()

def dezenas_mais_sorteadas(limit=20):
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

def dezenas_menos_sorteadas(limit=20):
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
    resultado
