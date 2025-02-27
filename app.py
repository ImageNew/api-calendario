from flask import Flask, jsonify

app = Flask(__name__)

# Simulação de eventos comemorativos
eventos = [
    {"data": "01-01", "evento": "Confraternização Universal"},
    {"data": "25-12", "evento": "Natal"},
    {"data": "07-09", "evento": "Independência do Brasil"},
]

@app.route('/eventos', methods=['GET'])
def get_eventos():
    return jsonify(eventos)

@app.route('/eventos/<data>', methods=['GET'])
def get_evento_por_data(data):
    evento = [e for e in eventos if e["data"] == data]
    if evento:
        return jsonify(evento)
return jsonify({"erro": "Nenhum evento encontrado"})
