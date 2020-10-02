import random
from flask import Flask, request
from pymessenger.bot import Bot
from pymessenger import Element, Button
from flask_ngrok import run_with_ngrok
from pymongo import MongoClient
from pymongo.collection import ObjectId
from random import randint
from datetime import datetime
import json
from wit import Wit


wit_access_token = "IH6LCI4GFDC3GHAS635WBKUSYKWFY2MT"
witclient = Wit(wit_access_token)

client = MongoClient("mongodb+srv://user:pwd@cluster0.pqawv.mongodb.net/<dbname>?retryWrites=true&w=majority")

db = client.get_database("data")

class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)


def getwit(message):
    
    resp = witclient.message(message)

    # print('Yay, got Wit.ai response: ' + str(resp))
    # print ("****************************")
    # js = str(resp).replace("'", '"')
    # print (js)
    # jres = json.loads(js)

    intentlist = []
    contactnames = []
    numbers = []
    medications = []
    durations = []
    qdos = []
    slevels = []
    mbody = " "
    dt = []
    for i in resp['intents']:
        print (i)
        if 'name' in i:
            print (i['name'])
            intentlist.append(i['name'])
    print ("****************************")

    if 'wit$contact:contact' in resp['entities']: 
        for i in resp['entities']['wit$contact:contact']:
            print(i)
            contactnames.append(i['body'])
            # print(resp['entities']['wit$contact:contact'])
        
    if 'wit$number:number' in resp['entities']: 
        print ('numbers')
        for i in resp['entities']['wit$number:number']:
            print(i)
            numbers.append(i['body'])
    
    if 'medication:medication' in resp['entities']: 
        print ('medicines')
        for i in resp['entities']['medication:medication']:
            print(i)
            medications.append(i['body'])
    
    if 'wit$duration:duration' in resp['entities']: 
        print ('durations')
        for i in resp['entities']['wit$duration:duration']:
            print(i)
            durations.append(i['body'])
    
    if 'wit$quantity:quantity' in resp['entities']: 
        print ('dosage quantity')
        for i in resp['entities']['wit$quantity:quantity']:
            print(i)
            qdos.append(i['body'])
    
    if 'wit$volume:volume' in resp['entities']: 
        print ('dosage quantity')
        for i in resp['entities']['wit$volume:volume']:
            print(i)
            qdos.append(i['body'])

    if 'wit$message_body:message_body' in resp['entities']: 
        print ('message')
        for i in resp['entities']['wit$message_body:message_body']:
            print(i)
            mbody = mbody + " " +str(i['body'])
    
    if 'wit$datetime:datetime' in resp['entities']: 
        print ('datetime')
        for i in resp['entities']['wit$datetime:datetime']:
            print(i)
            dt.append(i['body'])
            
    
    if 'strictness_level:strictness_level' in resp['entities']: 
        print ('strictness')
        for i in resp['entities']['strictness_level:strictness_level']:
            print(i)
            slevels.append(i['body'])

    # for e in resp['entities']:
    #     print (e)
    #     if 'wit$contact:contact' in e:
    #         print (e[0])
    
    # entities = resp['entities']
    # intents = resp['intents']
    
    return intentlist, contactnames, numbers, medications, durations, qdos, slevels, mbody, dt




def generate_id():
    final = ""
    c = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    for i in range(0, 6):
        k = randint(0, 35)
        final += c[k]

    return final

def register_patient(name, fbid, role):
    userid = generate_id()
    k = {"name":name, "strictness":-1, "fbid":fbid, "userid":userid, "role":role}
    try:
        db.users.insert_one(k)
        return {"status":"success", "userid":userid}
    except:
        return {"status":"failed"}

def add_strictness(userid, strictness):
    try:
        db.users.update_one({"userid":userid}, {"$set":{"strictness":strictness}})
        return {"status":"success"}
    except:
        return {"status":"failed"}
def get_patient_data(userid):
    try:
        return JSONEncoder().encode(db.users.find_one({"userid":userid}))
    except :
        return {"status":"failed"}

def regenerate_id(userid):
    try:
        new_id = generate_id()
        db.users.update_one({"userid":userid}, {"$set":{"userid":new_id}})
        return {"status":"success", "new_id":new_id}
    except:
        return {"status":"failed"}

def add_prescription(userid, name, count, num_days, times, dosage):
    d = str(datetime.now())
    pres_id = generate_id()
    k = {"userid":userid, "pres_id":pres_id, "name":name, "count":count, "dosage":dosage, "num_days":num_days, "times":times, "remaining":count, "timestamp":d}
    try:
        db.pres.insert_one(k)
        return {"status":"success", "pres_id":pres_id}
    except:
        return {"status":"failed"}

def get_pres(name):
    try:
        return JSONEncoder().encode(db.pres.find_one({"name":name}))
    except :
        return {"status":"failed"}

def get_all_pres(userid):
    try:
        final = []
        for i in db.pres.find({"userid":userid}):
            final.append(i)
        return JSONEncoder().encode({"status":"success", "result":final})
    except :
        return {"status":"failed"}

def update_pres(name, inc):
    try:
        db.pres.update_one({"name":name}, {"$inc":{"remaining":inc}})
        return {"status":"success"}
    except:
        return {"status":"failed"}

def reset_pres(name):
    try:
        db.pres.update_one({"name":name}, {"$set":{"remaining":db.pres.find_one({"name":name})["daily_count"]}})
        return {"status":"success"}
    except:
        return {"status":"failed"}

def delete_pres(name):
    try:
        db.pres.remove({"name":name})
        return {"status":"success"}
    except:
        return {"status":"failed"}
app = Flask(__name__)
run_with_ngrok(app)

ACCESS_TOKEN = 'EAAS5l0bjXnABAG5h2QFubiJOGsScR4Xk9kt76iFTnfl6y3LbZAxFgkAxsUvpt4dRVkNJ30ZBPHUjINxbZCVVQZATHAf8EV5ZCIDZCsdra7wwK8vAUSocNu8aVjnHtafIMEVjQDEIAYTQnVEVREQZCC2bCBkRqZB3Hoabow6FkK7gy5Uyqawj1pa6MSmrNW2noVYZD'
VERIFY_TOKEN = 'FACEBOOKHACKATHONTEAMZERO'
bot = Bot(ACCESS_TOKEN)

# Importing standard route and two requst types: GET and POST.
# We will receive messages that Facebook sends our bot at this endpoint
@app.route('/', methods=['GET', 'POST'])
def receive_message():
    if request.method == 'GET':
        # Before allowing people to message your bot Facebook has implemented a verify token
        # that confirms all requests that your bot receives came from Facebook.
        token_sent = request.args.get("hub.verify_token")
        return verify_fb_token(token_sent)
    # If the request was not GET, it  must be POSTand we can just proceed with sending a message
    # back to user
    else:
            # get whatever message a user sent the bot
        output = request.get_json()
        for event in output['entry']:
            messaging = event['messaging']
            for message in messaging:
                if message.get('message'):
                    # Facebook Messenger ID for user so we know where to send response back to
                    recipient_id = message['sender']['id']
                    if message['message'].get('text'):
                        
                        k = message['message'].get('text')

                        ##wit handler

                        intents, contactnames , numbers, medicines, durations, quantities, strictness, messagebody, datetimes = getwit(k)



                        if db.users.find_one({"fbid":recipient_id}) == None:
                            send_message(recipient_id, " Hi there! I’m Angel, your personal medical assistant. I’m here to help you keep track of and remember to take your medications. To start off, what would you like me to call you?")
                            register_patient("", recipient_id, "")
                        else:
                            details = db.users.find_one({"fbid":recipient_id})
                            if details["name"] == "":
                                db.users.update_one({"fbid":recipient_id}, {"$set":{"name":k.lower()}})
                                send_message(recipient_id, "Hey " + k + ", Nice to meet you! Are you a doctor or a patient?")
                            elif details["role"] == "":
                                if "doctor" in k.lower():
                                    db.users.update_one({"fbid":recipient_id}, {"$set":{"role":"doctor"}})
                                    send_message(recipient_id, "Nice, you are now registered as a doctor.")
                                elif "patient" in k.lower():
                                    db.users.update_one({"fbid":recipient_id}, {"$set":{"role":"patient"}})
                                    send_message(recipient_id, "Nice, you are now registered as a patient. Here is your unique ID to share with your doctor: " + details["userid"])
                                else:
                                    send_message(recipient_id, "Hey " + k + ", Nice to meet you! Are you a doctor or a patient?")
                            else:
                                send_message(recipient_id, "Need to write the rest of the code.")


                        """
                        if message['message'].get('text') == "Hello":
                            print('here')
                            send_message(recipient_id, "Hi, are you a doctor or a patient?")
                        elif message['message'].get('text') == "Doctor":
                            print('here')
                            send_message(recipient_id, "Set")
                        elif message['message'].get('text') == "Patient":
                            print('here')
                            send_message(recipient_id, "Set")
                        else:
                            send_message(recipient_id, response_sent_text)"""

    return "Message Processed"


def verify_fb_token(token_sent):
    if token_sent == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    return 'Invalid verification token'


def get_message():
    sample_responses = ["You are stunning!", "We're proud of you",
                        "Keep on being you!", "We're greatful to know you :)"]
    # return selected item to the user
    return random.choice(sample_responses)

def send_message(recipient_id, response):
    bot.send_text_message(recipient_id, response)
    return "success"

def sendbt(recipient_id):
    buttons = []
    button = Button(title='Doctor', type='text')
    buttons.append(button)
    button = Button(title='Patient', type='text')
    buttons.append(button)
    text = 'Select your role '
    bot.send_button_message(recipient_id, text, buttons)

if __name__ == "__main__":
    app.run()