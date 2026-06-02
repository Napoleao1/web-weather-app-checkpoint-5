from flask import Flask, render_template, request
import requests

app = Flask(__name__)
API_KEY = "9912ca74209c9d0f6b037ec2c9b1cc41"


@app.route("/", methods=["GET", "POST"])
def index():
    clima = None
    erro = None

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
                else:
                    erro = "Cidade não encontrada!"
            except requests.exceptions.RequestException:
                erro = "Não foi possível conectar ao servidor de clima."
    return render_template("index.html", clima=clima, erro=erro)


if __name__ == "__main__":
    app.run(debug=True)