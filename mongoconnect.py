from pymongo import MongoClient as mongc
import os
from dotenv import load_dotenv
from datetime import datetime
from bson.objectid import ObjectId # binary JSON, needed to decode mongoDB object ids
import atexit
from encryption import encrypt, decrypt

load_dotenv()
user = os.getenv("mongouser")
pwd = os.getenv("mongopass")

def connector():
    mongo = mongc(f"mongodb://{user}:{pwd}@localhost:27017/")
    return mongo

mongo = connector()
db = mongo["health_management"]
patdata = db["patients"]
atexit.register(mongo.close)

def patientAddsData(username,name,age):
    patdata.update_one(
        {"_id":username},
        {
            "$set":{
                "name":name,
                "age":age,
                "updatedOn":datetime.now()
            },
            "$setOnInsert":{
                "createdOn":datetime.now()
            }
        },upsert=True) # will only create one record per id

def medAddsData(data):
    patdata.update_one(
        {"_id":data.get("username")},
        {
            "$set":{
                "disease":encrypt(data.get("disease")),
                "medicines":encrypt(data.get("medicines")),
                "notes":encrypt(data.get("notes")),
                "updatedOn":datetime.now()
            }
        },upsert=True)

def showpatients():
    patients =  list(patdata.find())
    for patient in patients:
        patient["disease"] = decrypt(patient.get("disease"))
        patient["medicines"] = decrypt(patient.get("medicines"))
        patient["notes"] = decrypt(patient.get("notes"))
    return patients

def individual(username):
    ipatient =  patdata.find_one({"_id":username})
    if ipatient:
        ipatient["disease"] = decrypt(ipatient.get("disease"))
        ipatient["medicines"] = decrypt(ipatient.get("medicines"))
        ipatient["notes"] = decrypt(ipatient.get("notes"))
    return ipatient

def checkencryption():
    return list(patdata.find())