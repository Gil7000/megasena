import sqlite3
from loteria_caixa import MegaSena

def salvar_resultados_mega_sena(concurso_inicial, concurso_final):
    # Conectar com o banco de dados
    conn = sqlite3.connect('megasena.db')
    cursor = conn.cursor()

    # Criar tabela de resultados, caso ela ainda não exista
    cursor.execute('''CREATE TABLE IF NOT EXISTS resultados
                      (concurso INTEGER PRIMARY KEY, data_sorteio TEXT, bola1 INTEGER, bola2 INTEGER, bola3 INTEGER,
                       bola4 INTEGER, bola5 INTEGER, bola6 INTEGER, acumulado BOOLEAN, valor_acumulado REAL,
                       acumulado_especial REAL)''')

    # Obter os resultados dos últimos 2583 concursos
    for concurso in range(concurso_inicial, concurso_final + 1):
        print(f'Salvando resultado do concurso {concurso}...')
        resultado_megasena = MegaSena(concurso)

        # Verificar se o resultado existe
        if not resultado_megasena.listaDezenas():
            print(f"Resultado não encontrado para o concurso {concurso}")
            continue

        # Extrair informações do resultado
        resultado = {}
        resultado['concurso'] = concurso
        resultado['data_sorteio'] = resultado_megasena.dataApuracao()
        resultado['bola1'], resultado['bola2'], resultado['bola3'], resultado['bola4'], resultado['bola5'], resultado['bola6'] = resultado_megasena.listaDezenas()
        resultado['acumulado'] = resultado_megasena.acumulado()
        resultado['valor_acumulado'] = resultado_megasena.valorAcumuladoProximoConcurso()
        resultado['acumulado_especial'] = resultado_megasena.valorAcumuladoConcursoEspecial()

        # Mostrar os valores que serão inseridos no banco de dados
        print(f"Valor do campo 'concurso' para inserir no banco de dados: {resultado['concurso']}")

        # Salvar resultado no banco de dados
        cursor.execute('INSERT OR IGNORE INTO resultados VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                   (resultado['concurso'], resultado['data_sorteio'], resultado['bola1'], resultado['bola2'],
                    resultado['bola3'], resultado['bola4'], resultado['bola5'], resultado['bola6'],
                    resultado['acumulado'], resultado.get('valor_acumulado'), resultado.get('acumulado_especial')))
        conn.commit()
    # Fechar a conexão com o banco de dados
    cursor.close()
    conn.close()

salvar_resultados_mega_sena(2587, 2594)
