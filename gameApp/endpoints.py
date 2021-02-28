from flask import request, make_response, jsonify, send_from_directory
from flask_restful import reqparse, Resource
from models import db, Experiments
import json
import tablib
from pathlib import Path

EXPERIMENT_FOLDER = "./experiments/"
JSON_FOLDER = EXPERIMENT_FOLDER + "json/"
XLS_FOLDER = EXPERIMENT_FOLDER + "xls/"

class HelloWorld(Resource):
    def get(self):
        return {'about': 'Hello world!'}

# Get a list of all the ids in the database
class FetchList(Resource):
    def get(self):
        experiments = Experiments.query.all()
        return Experiments.serialize_list(experiments), 200, {"Access-Control-Allow-Origin" : "*"} 

# Get using id of the excel file to be grabbed
class FetchExcel(Resource):
    def get(self, todo_id):
        response = send_from_directory(directory=XLS_FOLDER, filename="{}.xls".format(todo_id))
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['content-type'] = 'application/vnd.ms-excel'
        return response

class CreateEntry(Resource):

    # Save to json file, need brackets for tablib compatibility
    def save_to_json(self, json_data, id_num):
        Path('./experiments/json').mkdir(parents=True, exist_ok=True)
        with open(f"{JSON_FOLDER}{id_num}.json", "w+") as f:
            f.write(json.dumps(json_data))

    # Create the xls file and save locally a copy
    def save_to_xls(self, id_num):
        Path('./experiments/xls').mkdir(parents=True, exist_ok=True)
        xls_data = tablib.Dataset()
        json_data = json.load(open(f"{JSON_FOLDER}{id_num}.json"))
        data = json_data['data']

        xls_data.headers = list(data[0].keys())

        for row in data:
            r = [i for i in list(row.values())]
            xls_data.append(r)

        with open(f"{XLS_FOLDER}{id_num}.xls", "wb") as f:
            f.write(xls_data.export('xls'))

    # Save to entry to db to easily access
    # Returns id of entry
    def save_entry_to_db(self, data):
        personal_data = data['personal_info']
        experiment = Experiments(
            first_name=personal_data['first_name'], last_name=personal_data['last_name'], email=personal_data['email'], experiment_type=personal_data['experiment_type'])
        db.session.add(experiment)
        db.session.commit()

        return experiment.id

    def post(self):
        data = request.json
        id_num = self.save_entry_to_db(data)
        self.save_to_json(request.json, id_num)
        self.save_to_xls(id_num)

        return {'id' : id_num}, 201, {"Access-Control-Allow-Origin" : "*"}

    # Cross site origin stuff
    def options(self):
        return {}, 200, {"Access-Control-Allow-Origin" : "*", 'Access-Control-Allow-Headers' : "*", 'Access-Control-Allow-Methods': "*"}

class RemakeTable(Resource):
    def get(self):
        Experiments.__table__.drop(db.engine)
        db.create_all()

        return {"message": "Remake table experiments success"}, 200, {"Access-Control-Allow-Origin" : "*"}