# -*- coding: utf-8 -*-
import locale
from gerar_paginas_html import conectar_banco, desconectar_banco
from estatisticas import dezenas_nao_sorteadas_ha_mais_tempo
from estatisticas import dezenas_mais_sorteadas
from estatisticas import dezenas_menos_sorteadas
from estatisticas import combinacoes_4_mais_repetidas
from estatisticas import combinacoes_5_mais_repetidas, soma_numeros_mais_sorteados
from estatisticas import combinacoes_6_mais_repetidas, pares_impares
locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

def gerar_tabela_pares_impares(conteudo):
    tabela_html = "<table>\n"
    tabela_html += "<tr>\n"
    tabela_html += "<th>Numeros Pares</th>\n"
    tabela_html += "<th>Numeros Impares</th>\n"
    tabela_html += "</tr>\n"
    tabela_html += "<tr>\n"
    tabela_html += f"<td>{conteudo[0]}</td>\n"
    tabela_html += f"<td>{conteudo[1]}</td>\n"
    tabela_html += "</tr>\n"
    tabela_html += "</table>\n"
    return tabela_html

# def gerar_tabela_soma_numeros_mais_sorteados(soma):
#     tabela_html = "<table>\n"
#     tabela_html += "<tr>\n"
#     tabela_html += "<th>Soma dos numeros mais sorteados</th>\n"
#     tabela_html += "</tr>\n"
#     tabela_html += "<tr>\n"
#     tabela_html += f"<td>{soma}</td>\n"
#     tabela_html += "</tr>\n"
#     tabela_html += "</table>\n"
#     return tabela_html

def gerar_tabela_soma_numeros_mais_sorteados(conteudo):
    tabela_html = "<table>\n"
    tabela_html += "<tr>\n"
    tabela_html += "<th>Soma dos numeros mais sorteados</th>\n"
    tabela_html += "<th>Frequência</th>\n"
    tabela_html += "</tr>\n"
    
    for soma, frequencia in conteudo:
        tabela_html += "<tr>\n"
        tabela_html += f"<td>{soma}</td>\n"
        tabela_html += f"<td>{frequencia}</td>\n"
        tabela_html += "</tr>\n"

    tabela_html += "</table>\n"
    return tabela_html


def gerar_pagina_html(nome_funcao, tabela_html):
    nome_arquivo = f"{nome_funcao}.html"
    with open(nome_arquivo, "w") as arquivo_html:
        arquivo_html.write("<!DOCTYPE html>\n")
        arquivo_html.write("<html lang='pt-br'>\n")
        arquivo_html.write("<head>\n")
        arquivo_html.write("<meta charset='UTF-8'>\n")
        arquivo_html.write(f"<title>{nome_funcao}</title>\n")
        arquivo_html.write("<style>\n")
        arquivo_html.write("table {width: 100%; border-collapse: collapse;}\n")
        arquivo_html.write("th, td {padding: 8px; text-align: left; border-bottom: 1px solid #ddd;}\n")
        arquivo_html.write("</style>\n")
        arquivo_html.write("</head>\n")
        arquivo_html.write("<body>\n")
        arquivo_html.write(f"<h1>Resultados de {nome_funcao}</h1>\n")
        arquivo_html.write(tabela_html)
        arquivo_html.write("</body>\n")
        arquivo_html.write("</html>\n")

    print(f"Arquivo {nome_arquivo} gerado com sucesso!")


def gerar_tabela_dezenas_mais_sorteadas(conteudo):
    tabela_html = "<table>\n"
    tabela_html += "<tr>\n"
    tabela_html += "<th>Dezena</th>\n"
    tabela_html += "<th>Quantidade de vezes sorteada</th>\n"
    tabela_html += "</tr>\n"
    for dezena, count in conteudo:
        tabela_html += "<tr>\n"
        tabela_html += f"<td>{dezena}</td>\n"
        tabela_html += f"<td>{count}</td>\n"
        tabela_html += "</tr>\n"
    tabela_html += "</table>\n"
    return tabela_html

def gerar_tabela_dezenas_nao_sorteadas(conteudo):
    tabela_html = "<table>\n"
    tabela_html += "<tr>\n"
    tabela_html += "<th>Dezena</th>\n"
    tabela_html += "<th>Dias desde o &uacute;ltimo sorteio</th>\n"
    tabela_html += "<th>Data do &uacute;ltimo sorteio</th>\n"
    tabela_html += "</tr>\n"
    for dezena, dias_desde_ultimo_sorteio, data_sorteio in conteudo:
        tabela_html += "<tr>\n"
        tabela_html += f"<td>{dezena}</td>\n"
        tabela_html += f"<td>{dias_desde_ultimo_sorteio}</td>\n"
        tabela_html += f"<td>{data_sorteio}</td>\n"
        tabela_html += "</tr>\n"
    tabela_html += "</table>\n"
    return tabela_html

def gerar_tabela_dezenas_menos_sorteadas(conteudo):
    tabela_html = "<table>\n"
    tabela_html += "<tr>\n"
    tabela_html += "<th>Dezena</th>\n"
    tabela_html += "<th>Quantidade de vezes sorteada</th>\n"
    tabela_html += "</tr>\n"
    for dezena, count in conteudo:
        tabela_html += "<tr>\n"
        tabela_html += f"<td>{dezena}</td>\n"
        tabela_html += f"<td>{count}</td>\n"
        tabela_html += "</tr>\n"
    tabela_html += "</table>\n"
    return tabela_html

def gerar_tabela_combinacoes(conteudo):
    tabela_html = "<table>\n"
    tabela_html += "<tr>\n"
    tabela_html += "<th>Combinacao</th>\n"
    tabela_html += "<th>Quantidade de vezes repetida</th>\n"
    tabela_html += "</tr>\n"
    for combinacao, count in conteudo:
        tabela_html += "<tr>\n"
        tabela_html += f"<td>{combinacao}</td>\n"
        tabela_html += f"<td>{count}</td>\n"
        tabela_html += "</tr>\n"
    tabela_html += "</table>\n"
    return tabela_html

def criar_pagina_principal(lista_de_arquivos):
    nome_arquivo = "index.html"
    with open(nome_arquivo, "w") as arquivo_html:
        arquivo_html.write("<!DOCTYPE html>\n")
        arquivo_html.write("<html lang='pt-br'>\n")
        arquivo_html.write("<head>\n")
        arquivo_html.write("<meta charset='UTF-8'>\n")
        arquivo_html.write("<title>Estatísticas da Mega Sena</title>\n")
        arquivo_html.write("<style>\n")
        arquivo_html.write("body {font-family: Arial, sans-serif;}\n")
        arquivo_html.write(".sidebar {width: 200px; position: fixed; height: 100%; background-color: #f1f1f1; padding: 20px 10px;}\n")
        arquivo_html.write(".main {margin-left: 200px; padding: 20px;}\n")
        arquivo_html.write("nav a {display: block; padding: 10px; text-decoration: none; background-color: #f1f1f1;}\n")
        arquivo_html.write("nav a:hover {background-color: #ddd;}\n")
        arquivo_html.write("iframe {width: 100%; height: 800px; border: none;}\n")
        arquivo_html.write("</style>\n")
        arquivo_html.write("<script>\n")
        arquivo_html.write("function carregarPagina(url) {\n")
        arquivo_html.write("  document.getElementById('iframe').src = url;\n")
        arquivo_html.write("}\n")
        arquivo_html.write("</script>\n")
        arquivo_html.write("</head>\n")
        arquivo_html.write("<body>\n")
        arquivo_html.write("<div class='sidebar'>\n")
        arquivo_html.write("<h1>Estatisticas da Mega Sena</h1>\n")
        arquivo_html.write("<nav>\n")
        for arquivo in lista_de_arquivos:
            arquivo_html.write(f"<a href='javascript:void(0)' onclick=\"carregarPagina('{arquivo}')\">{arquivo.replace('.html', '').replace('_', ' ')}</a>\n")
        arquivo_html.write("</nav>\n")
        arquivo_html.write("</div>\n")
        arquivo_html.write("<div class='main'>\n")
        arquivo_html.write("<h2 style='margin-left: 20px; color:#168EA6;'>Resultado mais recente</h2>\n")        
        arquivo_html.write("<table>\n")

        # Conectando ao banco de dados e buscando o resultado mais recente
        conn, cursor = conectar_banco()
        cursor.execute("SELECT * FROM resultados ORDER BY 1 DESC LIMIT 1")
        resultado = cursor.fetchone()

        # Adicionando o resultado mais recente à tabela

        arrecadacao_formatada = locale.currency(resultado[8], grouping=True)
        ganhadores_formatados = locale.currency(resultado[9], grouping=True)
        premio_total_formatado = locale.currency(resultado[10], grouping=True)

        arquivo_html.write("<table style='border-collapse: collapse; width: 100%; margin-left: 2em;'>\n")
        arquivo_html.write("<tr style='border-bottom: 1px solid black;'>\n")
        arquivo_html.write("<th style='text-align: left; color:#168EA6;'>Data</th>\n")
        arquivo_html.write("<th style='text-align: left; color:#168EA6;'>Dezena 1</th>\n")
        arquivo_html.write("<th style='text-align: left; color:#168EA6;'>Dezena 2</th>\n")
        arquivo_html.write("<th style='text-align: left; color:#168EA6;'>Dezena 3</th>\n")
        arquivo_html.write("<th style='text-align: left; color:#168EA6;'>Dezena 4</th>\n")
        arquivo_html.write("<th style='text-align: left; color:#168EA6;'>Dezena 5</th>\n")
        arquivo_html.write("<th style='text-align: left; color:#168EA6;'>Dezena 6</th>\n")
        arquivo_html.write("<th style='text-align: left; color:#168EA6;'>Valor Acumulado</th>\n")
        arquivo_html.write("</tr>\n")
        arquivo_html.write(f"<tr>\n")
        arquivo_html.write(f"<td style='text-align: left; color:#2DAFAF;'>{resultado[1]}</td>\n")
        arquivo_html.write(f"<td style='text-align: left; color:#2DAFAF;'>{resultado[2]}</td>\n")
        arquivo_html.write(f"<td style='text-align: left; color:#2DAFAF;'>{resultado[3]}</td>\n")
        arquivo_html.write(f"<td style='text-align: left; color:#2DAFAF;'>{resultado[4]}</td>\n")
        arquivo_html.write(f"<td style='text-align: left; color:#2DAFAF;'>{resultado[5]}</td>\n")
        arquivo_html.write(f"<td style='text-align: left; color:#2DAFAF;'>{resultado[6]}</td>\n")
        arquivo_html.write(f"<td style='text-align: left; color:#2DAFAF;'>{resultado[7]}</td>\n")
        arquivo_html.write(f"<td style='text-align: left; color:#2DAFAF;'>{ganhadores_formatados}</td>\n")
        arquivo_html.write("</tr>\n")
        arquivo_html.write("</table>\n")


        arquivo_html.write("</table>\n")
        arquivo_html.write("<iframe id='iframe' src='dezenas_mais_sorteadas.html'></iframe>\n")
        arquivo_html.write("</div>\n")
        arquivo_html.write("</body>\n")
        arquivo_html.write("</html>\n")

        print(f"Arquivo {nome_arquivo} gerado com sucesso!")



if __name__ == "__main__":
    arquivos_gerados = []

    # Chame a função dezenas_mais_sorteadas e armazene o resultado
    resultado2 = dezenas_mais_sorteadas()

    # Gere a página HTML com o resultado
    gerar_pagina_html("dezenas_mais_sorteadas", gerar_tabela_dezenas_mais_sorteadas(resultado2))
    nome_arquivo = "dezenas_mais_sorteadas.html"
    arquivos_gerados.append(nome_arquivo)

    resultado3 = dezenas_menos_sorteadas()
    gerar_pagina_html("dezenas_menos_sorteadas", gerar_tabela_dezenas_menos_sorteadas(resultado3))
    nome_arquivo = "dezenas_menos_sorteadas.html"
    arquivos_gerados.append(nome_arquivo)    

    # Chame a função dezenas_nao_sorteadas_ha_mais_tempo e armazene o resultado
    resultado = dezenas_nao_sorteadas_ha_mais_tempo()
    # Gere a página HTML com o resultado
    gerar_pagina_html("dezenas_nao_sorteadas_ha_mais_tempo", gerar_tabela_dezenas_nao_sorteadas(resultado))
    nome_arquivo = "dezenas_nao_sorteadas_ha_mais_tempo.html"
    arquivos_gerados.append(nome_arquivo)
    resultado4 = combinacoes_4_mais_repetidas()
    resultado5 = combinacoes_5_mais_repetidas()
    resultado6 = combinacoes_6_mais_repetidas()
    gerar_pagina_html("combinacoes_4_mais_repetidas", gerar_tabela_combinacoes(resultado4))
    gerar_pagina_html("combinacoes_5_mais_repetidas", gerar_tabela_combinacoes(resultado5))
    gerar_pagina_html("combinacoes_6_mais_repetidas", gerar_tabela_combinacoes(resultado6))
    nome_arquivo = "combinacoes_4_mais_repetidas.html"
    arquivos_gerados.append(nome_arquivo)
    nome_arquivo = "combinacoes_5_mais_repetidas.html"
    arquivos_gerados.append(nome_arquivo)
    nome_arquivo = "combinacoes_6_mais_repetidas.html"
    arquivos_gerados.append(nome_arquivo)

    resultado_pares_impares = pares_impares()

    # Gere a página HTML com o resultado
    gerar_pagina_html("pares_impares", gerar_tabela_pares_impares(resultado_pares_impares))
    nome_arquivo = "pares_impares.html"
    arquivos_gerados.append(nome_arquivo)

    resultado_soma_numeros_mais_sorteados = soma_numeros_mais_sorteados()
    gerar_pagina_html("soma_numeros_mais_sorteados", gerar_tabela_soma_numeros_mais_sorteados(resultado_soma_numeros_mais_sorteados))
    nome_arquivo = "soma_numeros_mais_sorteados.html"
    arquivos_gerados.append(nome_arquivo)



    criar_pagina_principal(arquivos_gerados)
