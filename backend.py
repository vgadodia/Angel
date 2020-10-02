from pymongo import MongoClient
from pymongo.collection import ObjectId
from random import randint
from datetime import datetime
import json

client = MongoClient("mongodb+srv://user:pwd@cluster0.pqawv.mongodb.net/<dbname>?retryWrites=true&w=majority")

db = client.get_database("data")

class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)


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
#print(register_patient("Nand", 0.5, "213908"))

#print(get_patient_data("ng8ax9"))

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
#print(add_prescription("ng8ax9", "crocin", 3, 14, [1200, 1300, 1400]))
#print(get_pres("2nozps"))

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

def get_notifications(time):
    num_tot = 0

    final = []
    x = []
    for i in db.pres.find():
        final.append(i)
    
    for i in final:
        
        if i["times"][int(i["count"]/7) - int(i["remaining"]/7)] > time +  + (int(db.users.find_one({"userid":i["userid"]})["strictness"]) * 60):
            x.append({"prescription_id":i["pres_id"], "userid":i["userid"]})
            num_tot += 1
    return {"number of responses":num_tot, "notifications":x}




print(get_notifications(1000))

#print(delete_pres("crocin"))
#print(add_prescription("ng8ax9", "crocin", 7, 14, [1200], "2 pills"))

#print(reset_pres("crocin"))

#print(get_patient_data("x8ndmj"))
