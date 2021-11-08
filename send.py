
import requests


import os
from azure.eventgrid import EventGridPublisherClient, EventGridEvent
from azure.core.credentials import AzureKeyCredential

topic_key = "Dk0U6BODZV9xVn4dr0wD9YcUXekLAGonX83V8CHLQNw="
endpoint = "https://sampleforgrid1.eastus-1.eventgrid.azure.net/api/events"

credential = AzureKeyCredential(topic_key)
client = EventGridPublisherClient(endpoint, credential)

client.send([
	EventGridEvent(
		event_type="Contoso.Items.ItemReceived",
		data={
			"itemSku": "Contoso Item SKU #1"
		},
		subject="Stand up",
		data_version="2.0"
	)
])

exit()


## Commands for cURL
'''

endpoint=$(az eventgrid topic show --name sampleforgrid1 -g rg-data-dev --query "endpoint" --output tsv)
key=$(az eventgrid topic key list --name sampleforgrid1 -g rg-data-dev --query "key1" --output tsv)

event='[ {"id": "'"$RANDOM"'", "eventType": "recordInserted", "subject": "myapp/vehicles/motorcycles", "eventTime": "'`date +%Y-%m-%dT%H:%M:%S%z`'", "data":{ "make": "Ducati", "model": "Monster"},"dataVersion": "1.0"} ]'

curl -X POST -H "aeg-sas-key: $key" -d "$event" $endpoint

'''

key = "Dk0U6BODZV9xVn4dr0wD9YcUXekLAGonX83V8CHLQNw="
endpoint = "https://sampleforgrid1.eastus-1.eventgrid.azure.net"

# key = os.environ["EG_ACCESS_KEY"]
# endpoint = os.environ["EG_TOPIC_HOSTNAME"]

event_json = {
    "id": "1", 
    "eventType": "recordInserted", 
    "subject": "myapp/vehicles/motorcycles", 
    "eventTime": "'`date +%Y-%m-%dT%H:%M:%S%z`'", 
    "data":
        { 
            "make": "Ducati", 
            "model": "Monster"
        },
    "dataVersion": "1.0"}

headers = {'aeg-sas-key': key}
res = requests.post(endpoint, data=event_json, headers=headers)

# event = EventGridEvent(
#     data={"team": "azure-sdk"},
#     subject="Door1",
#     event_type="Azure.Sdk.Demo",
#     data_version="2.0"
# )

# credential = AzureKeyCredential(key)
# client = EventGridPublisherClient(endpoint, credential)

# client.send(event)
