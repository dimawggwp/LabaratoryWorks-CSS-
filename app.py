from flask import Flask, jsonify
from flasgger import Swagger

app = Flask(__name__)
swagger = Swagger(app)
@app.route('/sum')
def sum_ab():
    a = 5
    b = 3
    return str(a + b)
@app.route('/')
def home():
    return "Сервер работает"
if __name__ == '__main__':
    app.run(port=5000)