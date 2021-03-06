from flask import Flask, request
from flask_restful import Api
from models import db, Experiments
from pathlib import Path

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///experiments.db'

db.init_app(app)
api = Api(app)

@app.after_request

# Cross site origin
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response

with app.app_context():
    db.create_all()

from endpoints import Home, FetchList, FetchExcel, CreateEntry, DeleteEntry, RemakeTable
api.add_resource(Home, '/')
api.add_resource(FetchExcel, '/fetchxls/<xls_id>')
api.add_resource(CreateEntry, '/create')
api.add_resource(DeleteEntry, '/delete/<id_num>')
api.add_resource(FetchList, '/list')
api.add_resource(RemakeTable, '/remakeTable')

if __name__ == '__main__':
    Path('./experiments/json').mkdir(parents=True, exist_ok=True)
    Path('./experiments/xls').mkdir(parents=True, exist_ok=True)
    app.run(debug=True)