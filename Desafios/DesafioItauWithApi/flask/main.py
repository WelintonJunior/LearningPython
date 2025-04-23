from flask import Flask, request,  make_response, jsonify
from models import Transaction, Statistics
from datetime import datetime, timedelta

app = Flask(__name__)

transactions = []

@app.route("/transacao", methods=["POST", "DELETE"])
def transacao():
    if request.method == "POST":
        data = request.get_data()

        if not data:
            return make_response("", 400)

        data = request.get_json()

        if not data:
            return make_response("", 400)

        value = data.get('value')
        dateHour = data.get('dateHour')

        if value is None or value == "" or not isinstance(value, (int, float)) or value < 0:
            return make_response("", 422)

        if not dateHour:
            return make_response("", 422)
        
        try:
            date_obj = datetime.fromisoformat(dateHour)
        except ValueError:
            return make_response(jsonify(message="Formato de data inválido"), 400)

        transaction = Transaction(value, date_obj)
        transactions.append(transaction)
        return "", 201
    elif request.method == "DELETE":
        transactions.clear()
        return "", 200
    
@app.get("/estatistica")
def estatistica():
    now = datetime.now().astimezone()  
    sixty_seconds_ago = now - timedelta(seconds=60)

    recent_transactions = [
        t for t in transactions if t.dateHour >= sixty_seconds_ago
    ]

    statistics = Statistics(recent_transactions)
    return make_response(jsonify(statistics.to_dict()), 200)

if __name__ == "__main__":
    app.run(debug=True)