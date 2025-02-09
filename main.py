from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

def obter_liturgia():
    url = "https://liturgia.cancaonova.com/pb/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    cor_liturgica = soup.select_one(".cor-liturgica")
    cor_liturgica = cor_liturgica.text.strip() if cor_liturgica else "Não encontrado"

    celebracao = soup.select_one(".entry-title")
    celebracao = celebracao.text.strip() if celebracao else "Não encontrado"

    def extrair_leitura(id_leitura):
        leitura = soup.select_one(f'#{id_leitura} .referencia')
        return leitura.text.strip() if leitura else "Não encontrado"

    dados = {
        "cor_liturgica": cor_liturgica,
        "celebracao": celebracao,
        "1_leitura": extrair_leitura("lit-1"),
        "salmo": extrair_leitura("lit-2"),
        "2_leitura": extrair_leitura("lit-3"),
        "evangelho": extrair_leitura("lit-4"),
    }

    return dados

@app.route("/liturgia", methods=["GET"])
def liturgia():
    return jsonify(obter_liturgia())

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
