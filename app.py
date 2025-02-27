from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

def pegar_eventos():
    url = "https://www.calendarr.com/brasil/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    resposta = requests.get(url, headers=headers)
    if resposta.status_code != 200:
        return {"erro": "Não foi possível acessar o site"}

    soup = BeautifulSoup(resposta.text, "html.parser")
    
    eventos = []
    for evento in soup.select(".list-unstyled li"):
        data = evento.select_one(".event-date")
        nome = evento.select_one(".event-title a")
        
        if data and nome:
            eventos.append({
                "data": data.text.strip(),
                "evento": nome.text.strip()
            })

    return eventos

@app.route('/eventos', methods=['GET'])
def get_eventos():
    """Retorna os eventos diretamente do site Calendarr"""
    eventos = pegar_eventos()
    return jsonify(eventos)

@app.route('/eventos/<data>', methods=['GET'])
def get_evento_por_data(data):
    """Busca um evento por data (formato: DD-MM)"""
    eventos = pegar_eventos()
    evento_filtrado = [e for e in eventos if e["data"] == data]
    
    if evento_filtrado:
        return jsonify(evento_filtrado)
    
    return jsonify({"erro": "Nenhum evento encontrado"}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
