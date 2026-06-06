from flask import Flask, render_template, request
import requests
from datetime import datetime, timezone, timedelta
import json
import os


app = Flask(__name__)
API_KEY = "9912ca74209c9d0f6b037ec2c9b1cc41"
HISTORICO_ARQUIVO = "historico.json"

def carregar_historico():
    if os.path.exists(HISTORICO_ARQUIVO):
        with open(HISTORICO_ARQUIVO, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


def salvar_historico(historico):
    with open(HISTORICO_ARQUIVO, "w", encoding="utf-8") as f:
        json.dump(historico, f, ensure_ascii=False, indent=2)

@app.route("/", methods=["GET", "POST"])
def index():
    clima = None
    erro = None
    nascer_sol = None
    por_sol = None
    historico = carregar_historico()



    if request.method == "POST":
        cidade = request.form.get("cidade")
        
        if cidade:
            url = "https://api.openweathermap.org/data/2.5/weather"
            params = {
                "q": cidade,
                "appid": API_KEY,
                "units": "metric",
                "lang": "pt_br",
            }
            try:
                resposta = requests.get(url, params=params)
                if resposta.status_code == 200:
                    clima = resposta.json()
                    fuso = timedelta(seconds=clima['timezone'])
                    nascer = datetime.fromtimestamp(clima['sys']['sunrise'], tz=timezone.utc) + fuso
                    por = datetime.fromtimestamp(clima['sys']['sunset'], tz=timezone.utc) + fuso
                    nascer_sol = nascer.strftime('%H:%M')
                    por_sol = por.strftime('%H:%M')
                    nome_cidade = clima['name']
                    if nome_cidade in historico:
                        historico.remove(nome_cidade)
                    historico.insert(0, nome_cidade)
                    historico = historico[:3]
                    salvar_historico(historico)


                else:
                    erro = "Cidade não encontrada!"
            except requests.exceptions.RequestException:
                erro = "Não foi possível conectar ao servidor de clima."
    return render_template("index.html", clima=clima, erro=erro, nascer_sol=nascer_sol, por_sol=por_sol, historico=historico)


if __name__ == "__main__":
    app.run(debug=True)