from flask import Flask, request
import sqlite3
import models
import models.models as models

app = Flask(__name__)

with sqlite3.connect("loja.db") as conn:
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            value REAL NOT NULL
        )
    ''')
    conn.commit()

@app.route("/product", methods=["POST", "GET", "PUT", "DELETE"])
def product():
    if request.method == "POST":
        data = request.get_json()
        if not data:
            return "Dados ausentes ou inválidos", 400

        name = data.get('name')
        value = data.get('value')

        if not name or value is None:
            return "Nome ou valor ausente", 400

        with sqlite3.connect("loja.db") as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO products (name, value) VALUES (?, ?)", (name, value))
            conn.commit()
        
        return "Produto criado com sucesso", 201
    elif request.method == "GET":
        id = request.args.get("id")
        if not id:
            return "Id não informado na url", 400
    
        try:
            id = int(id)
        except ValueError:
            return "Id inválido", 400
    
        with sqlite3.connect("loja.db") as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM products WHERE id = ?", (id,))
            product = cursor.fetchone()
    
        if product:
            return models.Product(product[0], product[1], product[2]).to_dict(), 200
        else:
            return "Produto não encontrado", 404
    elif request.method == "PUT":
        id = request.args.get("id")
        if not id:
            return "Id não informado na url", 400
    
        try:
            id = int(id)
        except ValueError:
            return "Id inválido", 400
        
        data = request.get_json()
        if not data:
            return "Json enviado é invalido", 400
        
        name = data.get('name')
        value = data.get('value')

        with sqlite3.connect("loja.db") as conn:
            cursor = conn.cursor()
            cursor.execute("update products set name = ?, value = ? where id = ?", (name, value, id))
            conn.commit()
            cursor.execute("select * from products where id = ?", (id,))
            product = cursor.fetchone()
        
        if product:
            return models.Product(product[0], product[1], product[2]).to_dict(), 200
        else:
            return "Produto não atualizado", 500
    elif request.method == "DELETE":
        id = request.args.get("id")

        if not id:
            return "Id não enviado na url", 400
        
        try:
            id = int(id)
        except ValueError:
            return "Id inválido", 400
        
        with sqlite3.connect("loja.db") as conn:
            cursor = conn.cursor()
            cursor.execute("delete from products where id = ?", (id,))
            conn.commit()
        
        return "Produto deletado com sucesso", 200
        
if __name__ == "__main__":
    app.run(debug=True)
