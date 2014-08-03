import predictionio

client = predictionio.Client(appkey="2JiIbLISTHDAt26H8acuZpDPcnUcF27Q8dzZswOCsFCyuKjS2m8K3YnKkGBEzMZF")

# Recommend 5 items to each user
user_ids = ["b.rakova@gmail.com"]
for user_id in user_ids:
    print "Retrieve 5 ranked messages for user", user_id
    try:
        client.identify(user_id)
        ranked = client.get_itemrank_ranked("rankingEngine", [
            "53cb223577b42f2976165de7", #Dropbox, openned, no reply
            "53cb223477b42f2976165d7d", #Amazon - not opened
        	"53cb223577b42f2976165dd2", #AWARE email - replied to in a long thread
        	"53cb223477b42f2976165d9d", #Amazon - not opened
        	"53cb223577b42f2976165ddc"]) #Iliya, replied to in a short thread
        print ranked
    except predictionio.ItemRecNotFoundError as e:
        print 'Caught exception:', e.strerror()