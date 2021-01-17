from flask import Flask, request
from flask_restful import Api
from models import db, Experiments
from pathlib import Path

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///experiments.db'

db.init_app(app)
api = Api(app)

with app.app_context():
    db.create_all()

from endpoints import HelloWorld, FetchList, FetchExcel, CreateEntry
api.add_resource(HelloWorld, '/')
api.add_resource(FetchExcel, '/fetchxls/<todo_id>')
api.add_resource(CreateEntry, '/create')
api.add_resource(FetchList, '/list')

if __name__ == '__main__':
    Path('./experiments/json').mkdir(parents=True, exist_ok=True)
    Path('./experiments/xls').mkdir(parents=True, exist_ok=True)
    app.run(debug=True)