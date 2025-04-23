from flask import Flask, render_template, request

# Create an instance of the Flask class

###WSGI Application
app = Flask(__name__)

@app.route("/")
def wlcome():
    return "<html><h1>H! TEXT</h1></html>"

@app.route("/index", methods=['GET'])
def index():
    return render_template('index.html')

@app.route("/about")
def about():
    return render_template('about.html')

@app.route("/form", methods=['GET', 'POST'])
def form():
    if request.method == 'GET':
        return render_template('form.html')
    elif request.method == 'POST':
        data = request.get_json()
        return f'Hello {data.get('name')}'
# @app.route("/transacao", methods=['GET', 'POST'])
# def transacao():
#     if request.method=='POST':
#         return "post transacao feita"
#     elif request.method=='GET':
#         return "get transacao feita"

# @app.get("/nome")
# def nome():
#     return "welinton"

if __name__ == "__main__":
    app.run(debug=True)