import requests
from bs4 import BeautifulSoup

def pegar_eventos():
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
