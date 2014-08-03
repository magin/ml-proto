import random
import json
import predictionio
import string

# Our PredictionIO Client
client = predictionio.Client(appkey="2JiIbLISTHDAt26H8acuZpDPcnUcF27Q8dzZswOCsFCyuKjS2m8K3YnKkGBEzMZF")

# Load Training Data
json_data = open('data-1000-items.json')
data = json.load(json_data)
json_data.close()

users = []
# items = []
# actions = []

def createUser(name, address):
	client.create_user(address.encode("UTF-8"), {"name": name.encode("UTF-8"),"email": address.encode("UTF-8")})

def createMessageItem(item): 
	itemToSave = { 
		"id" : item["_id"].encode("UTF-8"),
		"folderId": item["folderId"].encode("UTF-8"),
		"hasAttachments": not(not item["attachmentsList"] or len(item["attachmentsList"]) == 0),
		"date": item["date"].encode("UTF-8"),
		"subject": item["headers"]["subject"].encode("UTF-8"),
		"thrid": item["thrid"].encode("UTF-8"),
		"msgid": item["msgid"].encode("UTF-8"),
		"labels": item["labels"],
		"flags": item["flags"]
	}
	# items.append(itemToSave) - If we need it in the memory
	client.create_item(item["_id"], ("message",), itemToSave)

for item in data:
	if "folderId" not in item: 
		continue; #ignore bad items
	elif "subject" not in item["headers"]: 
		continue; #ignore bad items

	# Add new users
	if "from" in item.keys():		
		for userItem in item["from"]:	
			if "address" not in userItem:
				continue;
			address = userItem["address"]
			if address not in users:
				users.append(address)
				createUser(userItem["name"], address)
				#print "Adding new user: " + address

	if "to" in item.keys():
		for userItem in item["to"]:	
			if "address" not in userItem:
				continue;
			address = userItem["address"]
			if address not in users:
				users.append(address)
				createUser(userItem["name"], address)
				#print "Adding new user: " + address

	# Add new messages
	createMessageItem(item)

	# Add new actions
	fromUserId = item["from"][0]["address"]
	hasLabelSeen = "\\Seen" in item["flags"]
	hasBeenStarred = "\\Flagged" in item["flags"]
	hasReplied = "Re" in item["headers"]["subject"]
	# deleted flag

	client.identify(fromUserId)
	
	if hasLabelSeen: #The user has seen the email
		client.record_action_on_item("view", item["_id"])
	else: #The user has not even opened the email
		client.record_action_on_item("dislike", item["_id"])

	if hasBeenStarred: #The user has starred the email
		client.record_action_on_item("like", item["_id"])

	if hasReplied: #The user has starred the email
		client.record_action_on_item("conversion", item["_id"])

client.close()