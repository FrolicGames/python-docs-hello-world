import json
from flask import Flask, request, jsonify, Response
from flask_cors import CORS, cross_origin

import requests
import os
from azure.eventgrid import EventGridPublisherClient, EventGridEvent
from azure.core.credentials import AzureKeyCredential
from tinydb import TinyDB, Query

# print('ff')

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

global client

## API Token
# 00AG1sS2H77zZPsJeuFibp6QOewZk88qnjdONHJ0e6
# rk8r7rju



topic_key = "Dk0U6BODZV9xVn4dr0wD9YcUXekLAGonX83V8CHLQNw="
endpoint = "https://sampleforgrid1.eastus-1.eventgrid.azure.net/api/events"
credential = AzureKeyCredential(topic_key)
client = EventGridPublisherClient(endpoint, credential)



@app.route("/", methods=['GET', 'POST'])
@cross_origin()
def hello():
    # return "Hello, Azure!"
    try:
        name = request.json['name']
    except:
        return jsonify({'returned': 'nullin'})

    
    name = name.upper()+str(len(name))

    client.send([
        EventGridEvent(
            event_type="Contoso.Items.ItemReceived",
            data={
                "item": name
            },
            subject="Test Process",
            data_version="2.0"
        )
    ])


    return jsonify({'returned': name})

# 3 
@app.route('/webhook', methods=['POST', 'GET'])
def respond():
    ## Here we can process our request for event consumption
    ## endpoint url: https://backpoint.azurewebsites.net/webhook
    # https://d1a8-39-41-124-213.ngrok.io/webhook 

    # https://192.168.10.10:5000/webhook

    print(request)

    print()

    print('validation event', request.json[0]['data'])

    # 'eventType': 'Microsoft.EventGrid.SubscriptionValidationEvent'

    print(dict(request.args))

    if request.json[0]['eventType'] == 'Microsoft.EventGrid.SubscriptionValidationEvent':
        
        print('received a validation event')
        valtoken = request.json[0]['data']['validationCode']
        data = { "validationResponse": valtoken }
        resp = app.response_class(response=json.dumps(data), status=200, mimetype='plain/text')
        
        print('\n', data, '\n')

        return resp

    ## Response in case of normal events
    return Response(status=200)


@app.route("/history", methods=['GET'])
def view_logs():
    ## Example for query
    # http://127.0.0.1:5000/history?user=10
    
    # here we want to get the value of user (i.e. ?user=some-value)
    user = request.args.get('user')
    User = Query()

    # # creating connection Object which will contain SQL Server Connection    
    # connection = pypyodbc.connect('Driver={SQL Server};Server=.;Database=Employee;uid=sa;pwd=sA1234')# Creating Cursor    
        
    # cursor = connection.cursor()    
    # cursor.execute("SELECT * FROM EmployeeMaster")   
    db = TinyDB('user_logs.json')
    # all_recs = db.all()
    all_recs = db.search((User.uid == user))

    # print(all_recs)

    s = "<table style='border:1px solid red'>"    
    s = s + "<tr>"    
    s = s + "<td> UID </td>"
    s = s + "<td> Event Data </td>"
    
    for row in all_recs:    
        s = s + "<tr>"    
        for x in row:    
            s = s + "<td>" + str(row[x]) + "</td>"    
    
        s = s + "</tr>"    
    # connection.close()    
    
    # @app.route('/')    
    # @app.route('/home')    
    # def home():    
        
    return "<html><body>" + s + "</body></html>" 

    

# app.run(debug=True)

'''
cd OneDrive\Desktop\RevDigi\python-docs-hello-world
.venv\Scripts\activate.bat

az webapp up --sku B1 --name backpoint

pip --trusted-host=pypi.python.org --trusted-host=pypi.org --trusted-host=files.pythonhosted.org install <some_package>

## Event Grid Setup
az eventgrid domain --create --resource-group rg-data-dev --name sampleforgrid1
'''

