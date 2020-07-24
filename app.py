from flask import Flask,request, jsonify
from flask_cors import CORS
from flask_pymongo import PyMongo
from bson import ObjectId
import json

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/test"
mongo = PyMongo(app)
CORS(app)
db = mongo.db.test 

@app.route('/',methods=["GET","POST"])
def getpost():
    if request.method == "GET":
        object = []
        for i in db.find():
            object.append({
                "_ID":str(ObjectId(i["_id"])),
                "note":i["note"],
                "date":i["date"],
                "time":i["time"]
            })
        return jsonify(object)
    elif request.method == "POST":
       id = db.insert({
           "note": request.json["note"],
           "date": request.json["date"],
           "time": request.json["time"] 
        })
    return  jsonify(str(ObjectId(id)))

@app.route('/<id>',methods=["DELETE","PUT"])
def delete(id):
    if request.method == "DELETE":
        db.delete_one({
            "_id": ObjectId(id)
        })
        return jsonify({"message": "Data Deleted."})
    elif request.method == "PUT":
        db.update({
            "_id": ObjectId(id)
        }, 
        {
            "$set": {
            "note": request.json["note"],
           "date": request.json["date"],
           "time": request.json["time"]
            }
        }
        )
    return jsonify({"message":"updated"})
        
@app.route('/getone/<id>',methods=["GET"])
def getone(id):
  res= db.find_one({"_id":ObjectId(id)})
  print(res)
  return {"_ID":str(ObjectId(res["_id"])),
  "note": res["note"],
  "date": res['date'],
  "time": res['time']
  }
