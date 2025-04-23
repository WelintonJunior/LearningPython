from flask import Flask

# Create an instance of the Flask class

###WSGI Application
app = Flask(__name__)

@app.route("/")
def wlcome():
    return "First get route for sweb"

@app.route("/index")
def index():
    return "First get asdasdroute for sweb"

if __name__ == "__main__":
    app.run(debug=True)