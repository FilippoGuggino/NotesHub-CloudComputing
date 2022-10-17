import pymongo
import pprint
import json
from bson.json_util import dumps
from bson.json_util import loads
from ZooClient import ZooClient

#initialize ZooKeeper client
zk = ZooClient("172.16.1.191:2181, 172.16.2.40:2181")
mongoAddress, mongoPort = zk.getMongoAddress()

MONGO_SERVER = "mongodb://" + mongoAddress + ":" + mongoPort + "/"
MONGO_DB, MONGO_COLLECTION = zk.getMongoDbCollection()

client = pymongo.MongoClient(MONGO_SERVER)
#select db
db = client[MONGO_DB]
#select collection
collection = db[MONGO_COLLECTION]

def handle_request(request_json):
    request = json.loads(request_json)
    if request["requestType"] == "newNote":
        return new_note(request)
    if request["requestType"] == "deleteNote":
        return delete_note(request)
    if request["requestType"] == "findNotesByAuthor":
        return find_notes_by_author(request)
    if request["requestType"] == "findNotesByDate":
        return find_notes_by_date(request)
    if request["requestType"] == "findNotesBySubject":
        return find_notes_by_subject(request)
    if request["requestType"] == "getNoteByTitle":
        return get_note_by_title(request)
    if request["requestType"] == "updateNote":
        return update_note(request)
    return "Unexpected request"

def new_note(request):
    title = request['title']
    author = request['author']
    date = request['date']
    text = request['text']
    subject = request['subject']
    dict = {"title" : title, "author" : author, "date" : date, "text" : text, "subject" : subject}
    query = {"title" : title}
    #check if a note with the same title already exists
    if collection.count_documents(query) != 0:
        return "This title already exists"
    collection.insert_one(dict)
    return "The note has been inserted"

def delete_note(request):
    title = request['title']
    query = {"title" : title}
    docs = collection.find(query)
    if collection.count_documents(query) == 0:
        return "The note doesn't exist"
    collection.delete_one(query)
    return "The note has been deleted"

def find_notes_by_author(request):
    author = request['author']
    query = {"author" : author}
    if collection.count_documents(query) == 0:
        return "There are no notes with this author"
    docs = collection.find(query)
    return loads(dumps(docs))

def find_notes_by_date(request):
    date = request['date']
    query = {"date" : date}
    if collection.count_documents(query) == 0:
        return "There are no notes with this date"
    docs = collection.find(query)
    return loads(dumps(docs))

def find_notes_by_subject(request):
    subject = request['subject']
    query = {"subject" : subject}
    if collection.count_documents(query) == 0:
        return "There are no notes with this subject"
    docs = collection.find(query)
    return loads(dumps(docs))

def get_note_by_title(request):
    title = request['title']
    query = {"title" : title}
    docs = collection.find_one(query)
    if docs is None:
        return "There are no notes with this title"
    return loads(dumps(docs))

def update_note(request):
    title = request['title']
    author = request['author']
    date = request['date']
    text = request['text']
    subject = request['subject']
    query = {"title" : title}
    if collection.count_documents(query) == 0:
        return "There are no notes with this title, try to insert a new note"
    new_values = {"$set":{"author" : author, "date" : date, "text" : text, "subject" : subject}}
    collection.update_one(query, new_values)
    return "The note has been updated"
