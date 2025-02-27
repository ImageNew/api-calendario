from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup
import os

app = Flask(__name__)

def pegar_eventos():
    """Busca eventos diretamente do site Calendarr e retorna uma lista de eventos."""
    url = "https://www.calendarr.com/brasil/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Accept-Language": "pt-BR,pt;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8"
    }

    resposta = requests.get(url, headers=headers)
    if resposta.status_code != 200:
        return {"erro": f"Falha ao acessar o site. Código: {resposta.status_code}"}

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

    return eventos if eventos else {"erro": "Nenhum evento encontrado"}

@app.route('/eventos', methods=['GET'])
def get_eventos():
    """Retorna todos os eventos coletados do site Calendarr."""
    eventos = pegar_eventos()
    return jsonify(eventos)

@app.route('/eventos/<data>', methods=['GET'])
def get_evento_por_data(data):
    """Busca um evento por data no formato DD-MM"""
    eventos = pegar_eventos()
    evento_filtrado = [e for e in eventos if e["data"] == data]

    if evento_filtrado:
        return jsonify(evento_filtrado)

    return jsonify({"erro": "Nenhum evento encontrado"}), 404

# Configuração correta do Flask para rodar no Render
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))  # Render usa uma variável de ambiente para definir a porta
    app.run(host='0.0.0.0', port=port)
