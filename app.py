from flask import Flask, jsonify
import os

app = Flask(__name__)

# Simulação de eventos comemorativos
eventos = [
    {"data": "01-01", "evento": "Confraternização Universal"},
    {"data": "25-12", "evento": "Natal"},
    {"data": "07-09", "evento": "Independência do Brasil"},
]

@app.route('/eventos', methods=['GET'])
def get_eventos():
    """Retorna todos os eventos disponíveis."""
    return jsonify(eventos)

@app.route('/eventos/<data>', methods=['GET'])
def get_evento_por_data(data):
    """Busca evento por data (formato: DD-MM)"""
    evento = [e for e in eventos if e["data"] == data]
    if evento:
        return jsonify(evento)
    return jsonify({"erro": "Nenhum evento encontrado"}), 404

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))  # Usa a porta definida pelo Render
    app.run(host='0.0.0.0', port=port)
