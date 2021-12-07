
import requests
import json


testEndpoint = "https://api-ce.kroger.com/v1/"

clientID= "massimo-test-f12a257e3061335566696b004a3741eb5595607663175665324"
secret = "R4uh4Qa14u4qLfxezg5MTkLVqOne7bcBfz48tKRf"
base64Endoded = "bWFzc2ltby10ZXN0LWYxMmEyNTdlMzA2MTMzNTU2NjY5NmIwMDRhMzc0MWViNTU5NTYwNzY2MzE3NTY2NTMyNDpSNHVoNFFhMTR1NHFMZnhlemc1TVRrTFZxT25lN2JjQmZ6NDh0S1Jm"



nutritionixHeader = {
    "x-app-id": "0999f9b7",
    "x-app-key": "18c53f77afe57738f8e2fa85269a8269",
    "x-remote-user-id": "0"
    }



# this is getting authorization token
def getKrogerAuthenticationToken():
    url = 'https://api-ce.kroger.com/v1/connect/oauth2/token?grant_type=client_credentials&scope=product.compact'
    customHeaders = {
    "Content-Type": "application/x-www-form-urlencoded",
    "Authorization": "Basic bWFzc2ltby10ZXN0LWYxMmEyNTdlMzA2MTMzNTU2NjY5NmIwMDRhMzc0MWViNTU5NTYwNzY2MzE3NTY2NTMyNDpSNHVoNFFhMTR1NHFMZnhlemc1TVRrTFZxT25lN2JjQmZ6NDh0S1Jm"
    }
    r = requests.post(url, headers=customHeaders)
    token = json.loads(r.text)["access_token"]
    return token








# ok now I make a request to the metro mart by my house for meat, location code is 53400180
token = getKrogerAuthenticationToken()
authorization = "Bearer "+ token
#print(authorization)

# removed these for ease of tesing -- "pantry","dairy","deli","bakery","candy","eggs","breakfast"
listOfDepartments = ["fruit", "vegetable","meat","seafood"]


# need to iterate through all departments
# making it so that it only does curbside pickup options because thats what im gonna want, not sure if the csp part is actually working rn
categoryData = {}

for category in listOfDepartments:
    
    # need to paginate for all resultss using start and limit, currently cutting limit to 5 for testing ease -- max is 50
    url = "https://api-ce.kroger.com/v1/products?filter.term=" + category + "&filter.locationId=53400180&filter.limit=5&filter.fulfillment=csp"
    customHeaders = {
    "Content-Type": "application/json; charset=utf-8",
    "Authorization": authorization,
    "Cache-Control": "application/json; charset=utf-8"
    }
    r = requests.get(url, headers=customHeaders)
    #print(r.text)
    jsonForm = json.loads(r.text)
    categoryData[category] = jsonForm["data"]

#write products to json file, need to figure out how to delete file before updating otherwise will not override
with open("productsByCategory.json", "w") as productsFile:
    json.dump(categoryData, productsFile)




nutritionData = {}
nutHeaders = {
    "x-app-id": "0999f9b7",
    "x-app-key": "18c53f77afe57738f8e2fa85269a8269",
    "x-remote-user-id": "0"
    }
nutURL = "https://trackapi.nutritionix.com/v2/natural/nutrients"
# need to store this data im getting
for category in categoryData.keys():
    productData = categoryData[category]
    for product in productData:
        description = product["description"]

        #not sure why I thought it was relevent to have this line but whatevs.
        #fulfillmentOptions = product["items"][0]["fulfillment"]
 
        nutritionixBody = {
            "query":description,
            "timezone": "US/Eastern"
        }

        # r = requests.get(url, headers=customHeaders)
        # #print(r.text)
        # jsonForm = json.loads(r.text)
        # categoryData[category] = jsonForm["data"]




        nutritionInfo = requests.post(nutURL, headers=nutHeaders, data=nutritionixBody)
        jsonNut = json.loads(nutritionInfo.text)
        nutritionData["description"] = jsonNut
 

# now store the nutrition data in json file
#write products to json file
with open("productNutritionInfo.json", "w") as productsNut:
    json.dump(nutritionData, productsNut)



