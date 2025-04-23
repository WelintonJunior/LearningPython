from flask import Flask, request, jsonify
from models import db, ma, Product, ProductSchema

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
ma.init_app(app)

with app.app_context():
    db.create_all()

product_schema = ProductSchema()
products_schema = ProductSchema(many=True)

@app.route("/product", methods=["POST"])
def create_product():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Dados inválidos"}), 400

    try:
        product = product_schema.load(data)
        db.session.add(product)
        db.session.commit()
        return product_schema.jsonify(product), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route("/product", methods=["GET"])
def get_product():
    id = request.args.get("id")
    if not id:
        return jsonify({"error": "Id não informado"}), 400

    product = Product.query.get(id)
    if product:
        return product_schema.jsonify(product)
    else:
        return jsonify({"error": "Produto não encontrado"}), 404

@app.route("/product", methods=["PUT"])
def update_product():
    id = request.args.get("id")
    if not id:
        return jsonify({"error": "Id não informado"}), 400

    product = Product.query.get(id)
    if not product:
        return jsonify({"error": "Produto não encontrado"}), 404

    data = request.get_json()
    if not data:
        return jsonify({"error": "Dados inválidos"}), 400

    product.name = data.get("name", product.name)
    product.value = data.get("value", product.value)

    db.session.commit()
    return product_schema.jsonify(product)

@app.route("/product", methods=["DELETE"])
def delete_product():
    id = request.args.get("id")
    if not id:
        return jsonify({"error": "Id não informado"}), 400

    product = Product.query.get(id)
    if not product:
        return jsonify({"error": "Produto não encontrado"}), 404

    db.session.delete(product)
    db.session.commit()
    return jsonify({"message": "Produto deletado com sucesso"}), 200

if __name__ == "__main__":
    app.run(debug=True)
