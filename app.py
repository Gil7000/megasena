from flask import Flask, render_template
from estatisticas import dezenas_mais_sorteadas
from estatisticas import dezenas_menos_sorteadas
from estatisticas import dezenas_nao_sorteadas_ha_mais_tempo
from estatisticas import combinacoes_4_mais_repetidas
from estatisticas import combinacoes_5_mais_repetidas
from estatisticas import combinacoes_6_mais_repetidas

app = Flask(__name__)

estatisticas = [
    ('Dezenas mais sorteadas', dezenas_mais_sorteadas),
    ('Dezenas menos sorteadas', dezenas_menos_sorteadas),
    ('Dezenas não sorteadas há mais tempo', dezenas_nao_sorteadas_ha_mais_tempo),
    ('Combinações de 4 números mais repetidas', combinacoes_4_mais_repetidas),
    ('Combinações de 5 números mais repetidas', combinacoes_5_mais_repetidas),
    ('Combinações de 6 números mais repetidas', combinacoes_6_mais_repetidas)
]

@app.route('/')
def index():
    return render_template('index.html', estatisticas=estatisticas)
