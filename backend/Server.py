from email.mime import base
from urllib import request
from flask import Flask, request, Response, jsonify
from flask_cors import CORS
from flask_restful import Api
import base64
from PIL import Image
import io
import os
from main import *


customers_folder = "../collector/public/customers/"

create_tables()

app = Flask(__name__)
CORS(app)
api = Api(app)

print(os.getcwd())

@app.route('/', methods=['GET'])
def home():
    return "<h1>Evidence Collector Alpha version</p>"


# Returns the full list of customers
@app.route('/customer', methods=['GET'])
def Customers():
    if request.method == 'GET':
        customers = get_customers()
        return jsonify(customers)

# Returns the incidents of the customer <id>
@app.route('/customer/<id>', methods=['GET'])
def CustomerIncidents(id):
    if request.method == 'GET':
        incidents = get_customer_incidents(id)
        incidents = sorted(incidents, key=lambda x: x["date"], reverse=True)
        return jsonify(incidents)

# Creates a new customer
@app.route('/customer/create', methods=['POST'])
def createCustomer():
    if request.method == 'POST':
        content = request.get_json()
        ext = content["logo"].split("/")[1].split(";")[0]
        img = content["logo"].split("base64,")[1]
        customer = content["name"]
        logo_path = customers_folder + customer + "/"
        res = create_customer(content["name"], customer + "/logo." + ext)
        if res == 0 and "name" in content:
            if os.path.exists(logo_path) == False:
                os.makedirs(logo_path)
                print("creaing folder {}".format(logo_path))
            Image.open(io.BytesIO(base64.b64decode(img))).save(customers_folder + customer + "/logo." + ext)
            response = Response(status=201)
        else:
            response = Response(status=409)
        return response

# Deletes the customer
@app.route('/customer/<id>/delete', methods=['DELETE'])
def deleteCustomer(id):
    if request.method == 'DELETE':
        res = delete_customer(id)
        if res == 0:
            response = Response(status=200)
        else:
            response = Response(status=404)
        return response

# Return all the incidents
@app.route('/incident', methods=['GET'])
def getIncidents():
    if request.method == 'GET':
        incidents = get_incidents()
        incidents = sorted(incidents, key=lambda x: x["date"], reverse=True)
        return jsonify(incidents)

# Creates a new incident
@app.route('/incident/create', methods=['POST'])
def createIncident():
    if request.method == 'POST':
        content = request.get_json()
        res = create_incident(content["customerId"], content["date"], content["type"])
        if res == 0:
            response = Response(status=201)
        elif res == -2:
            response = Response(status=409)
        else:
            response = Response(status=404)
        return response


@app.route('/incident/<id>', methods=['GET'])
def getEvidences(id):
    if request.method == 'GET':
        evidences = get_incident_evidences(id)
        if evidences == -1 or evidences == {}:
            response = Response(status=404)
            return response
        else:
            return jsonify(evidences)

# Deletes an incident given the id
@app.route('/incident/<id>/delete', methods=['DELETE'])
def deleteIncident(id):
    if request.method == 'DELETE':
        res = delete_incident(id)
        if res == 0:
            response = Response(status=200)
        else:
            response = Response(status=404)
        return response

# Creates a new evidence
@app.route('/evidence/create', methods=['POST'])
def createEvidence():
    if request.method == 'POST':
        content = request.get_json()     
        ext = content["image"].split("/")[1].split(";")[0]
        img = content["image"].split("base64,")[1]
        customer = get_customer_name_from_id(get_customerId_from_incidentId(content["incidentId"]))

        count = 1
        evidence_path = "{}{}/{}/{}.{}".format(customers_folder, customer, content['incidentId'], count, ext)
        while os.path.exists(evidence_path):
            count += 1
            evidence_path = "{}{}/{}/{}.{}".format(customers_folder, customer, content['incidentId'], count, ext)
        
        relative_path = evidence_path.replace("../collector/public", "")
        res = create_evidence(content["incidentId"], content["gather_datetime"], content["datetime"], content["killchain"], content["host"], content["host_type"], relative_path, content["description"])
        if res == 0:
            if os.path.exists(os.path.dirname(evidence_path)) == False:
                os.makedirs(os.path.dirname(evidence_path))
            Image.open(io.BytesIO(base64.b64decode(img))).save(evidence_path)
            response = Response(status=201)
        else:
            response = Response(status=404)
        return response

# Deletes an evidence given an id
@app.route('/evidence/<id>/delete', methods=['DELETE'])
def deleteEvidence(id):
    if request.method == 'DELETE':
        res = delete_evidence(id)
        if res == 0:
            response = Response(status=200)
        else:
            response = Response(status=404)
        return response


@app.route('/evidence/update', methods=['PATCH'])
def updateEvidence():
    if request.method == 'PATCH':
        content = request.get_json()
        attributes = list(dict(content).keys())[1:]
        values = list(dict(content).values())[1:]
        res = update_evidence(content["evidenceId"], attributes, values)
        if res == -2:
            response = Response(status=400)
        elif res == -1:
            response = Response(status=404)
        else:
            response = Response(status=200)
        return response

# Gets the name of a customer given the id
@app.route('/customer/<id>/name', methods=['GET'])
def getCustomerName(id):
    if request.method == 'GET':
        content = request.get_json()
        response = get_customer_name_from_id(id)
        print(response)
        if response == -1:
            response = Response(status=404)
        return response

app.run()
