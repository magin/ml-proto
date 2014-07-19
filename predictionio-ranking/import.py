import random
import json
import predictionio

# Our PredictionIO Client
client = predictionio.Client(appkey="2JiIbLISTHDAt26H8acuZpDPcnUcF27Q8dzZswOCsFCyuKjS2m8K3YnKkGBEzMZF")

# Load Training Data
json_data = open('data.json')
data = json.load(json_data)
json_data.close()

users = []
items = []
actions = []

def createUser(name, address):
	client.create_user(address, {
		"name": name,
		"email": address
		# more user data if we have access to any
		})

def createMessageItem(item): 
    client.create_item(item["_id"], ("message",), { 
		"id" : item["_id"], 
		"custom": "value",
		"folderId": item["folderId"],
		"hasAttachments": not(not item["attachmentsList"] or len(item["attachmentsList"]) == 0),
		"date": item["date"],
		"subject": item["headers"]["subject"],
		"thrid": item["thrid"],
		"msgid": item["msgid"],
		"labels": item["labels"], # view if seen
		"flags": item["flags"]
	})

for item in data:
	# Add new users
	if "from" in item.keys():		
		for userItem in item["from"]:	
			address = userItem["address"]
			if address not in users:
				users.append(address)
				createUser(userItem["name"], address)
				print "Adding new user: " + address

	if "to" in item.keys():
		for userItem in item["to"]:	
			address = userItem["address"]
			if address not in users:
				users.append(address)
				createUser(userItem["name"], address)
				print "Adding new user: " + address

	# Add new messages
	createMessageItem(item)

	# Add new actions
	fromUserId = item["from"][0]["address"]
	hasLabelSeen = "\\Seen" in item["flags"]
	hasBeenStarred = "\\Flagged" in item["flags"]
	hasReplied = "Re" in item["headers"]["subject"]

	client.identify(fromUserId)
	if hasLabelSeen: #The user has read the email
		client.record_action_on_item("view", item["_id"])	
	if hasBeenStarred: #The user has starred the email
		client.record_action_on_item("like", item["_id"])
	if hasReplied: #The user has starred the email
		client.record_action_on_item("conversion", item["_id"])

client.close()