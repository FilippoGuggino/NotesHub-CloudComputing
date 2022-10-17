import connexion
import six
import pika
import json
import uuid

from kazoo.client import KazooClient
from swagger_server.models.note import Note  # noqa: E501
from swagger_server import util

#create unique id for Remote Procedure Call
#uniqueness is ensured by using MAC address
corr_id = str(uuid.uuid4())
response = None


#using zookeeper to retrieve rabbitMQ address
def getRabbitAddress():
    client = KazooClient(hosts="172.16.1.191:2181, 172.16.2.40:2181", read_only=True)
    client.start()
    ip, stats = client.get("/ip_addresses/rabbitmq/master")
    port, stats = client.get("/ports/rabbitmq")
    ip = ip.decode("utf-8")
    port = port.decode("utf-8")
    client.stop()
    return ip, port
    
#using zookeeper to retrieve routing key
def getQueueName():
    ipAddress = "172.16.1.191:2181, 172.16.2.40:2181"
    zk = KazooClient(hosts=ipAddress, read_only=True)
    zk.start()
    queue, stats = zk.get("/routing_key")
    queue = queue.decode("utf-8")
    zk.stop()
    return queue

def get_NOTE_MAX_LEN():
    client = KazooClient(hosts="172.16.1.191:2181, 172.16.2.40:2181", read_only=True)
    client.start()
    max_len, stats = client.get("/note_max_length")
    max_len.decode("utf-8")
    client.stop()
    return int(max_len)

def dispatchRequest(message):
    global corr_id
    global response

    response = None
    #connection to rabbitMQ -> it is in the controller machine 172.16.1.157
    #retrieving ip address and port of rabbitMq
    ip, port = getRabbitAddress()

    connection = pika.BlockingConnection(pika.ConnectionParameters(ip))
    channel = connection.channel()
    
    #if queue is empty then a name is automatically generated by RabbitMQ (saved into result.method.queue) 
    result = channel.queue_declare(queue='', exclusive=True)
    callback_queue = result.method.queue
    #remote procedure call -> RPC
    #define the function to call when a response arrive
    channel.basic_consume(queue=callback_queue,on_message_callback=on_response,auto_ack=True)

    message = json.dumps(message)
    channel.basic_publish(
            exchange='',
            routing_key=getQueueName(),
            properties=pika.BasicProperties(
            	#response from backend will be automatically sent to the callback_queue
                reply_to=callback_queue,
                correlation_id=corr_id,
            ),
            body=message)

	#wait for response from backend
    while response is None:
        connection.process_data_events()
    print(response.decode("utf-8"))

    return response.decode("utf-8")

def on_response(ch, method, props, body):
    global response
    global corr_id
    #use this condition to check if the response is for me
    if corr_id == props.correlation_id:
        response =  body

def convertNoteObjectToJson(object):
    title = object.title
    author = object.author
    date = object._date
    text = object.text
    subject = object.subject
    my_dict = {
    'title': title,
    'author': author,
    'date': date.strftime("%d %b, %Y"),
    'text': text,
    'subject': subject
    }

    my_json = json.dumps(my_dict, ensure_ascii=False)
    return my_json

def convertVariableToJson(variable,title):
    if title == 'date':
        variable = variable.strftime("%d %b, %Y")
    my_dict = {
        title: variable
    }
    my_json = json.dumps(my_dict, ensure_ascii=False)
    return my_json


def add_note(body):  # noqa: E501
    """Add a new note

     # noqa: E501

    :param body: The note that will be added
    :type body: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        body = Note.from_dict(connexion.request.get_json())  # noqa: E501
        if len(body.text) > get_NOTE_MAX_LEN():
            return 'Note length exceeds max size. The max size is: '+str(get_NOTE_MAX_LEN())
        print()
        print('adding note..')
        print('calling dispatch request...')

        jsonObject = json.loads(convertNoteObjectToJson(body))
        jsonObject['requestType']='newNote'
        print(jsonObject)
        return dispatchRequest(jsonObject)


        print('finished dispatch request call.')


def delete_note(noteTitle):  # noqa: E501
    """Deletes a note

     # noqa: E501

    :param noteTitle: Note id to delete
    :type noteTitle: str

    :rtype: None
    """
    print('deleting note..')
    print('calling dispatch request...')

    jsonObject = json.loads(convertVariableToJson(noteTitle,'title'))
    jsonObject['requestType'] = 'deleteNote'
    return dispatchRequest(jsonObject)



def find_notes_by_author(author):  # noqa: E501
    """Finds Notes by author

     # noqa: E501

    :param author:
    :type author: str

    :rtype: List[Note]
    """
    print('finding note by author..')
    print('calling dispatch request...')

    jsonObject = json.loads(convertVariableToJson(author,'author'))
    jsonObject['requestType'] = 'findNotesByAuthor'
    return dispatchRequest(jsonObject)



def find_notes_by_date(date):  # noqa: E501
    """Finds Notes by date

     # noqa: E501

    :param _date:
    :type _date: str

    :rtype: List[Note]
    """
    _date = util.deserialize_date(date)
    print('finding note by date..')
    print('calling dispatch request...')
    print('Date: '+str(_date))
    jsonObject = json.loads(convertVariableToJson(_date,'date'))
    jsonObject['requestType'] = 'findNotesByDate'
    return dispatchRequest(jsonObject)




def find_notes_by_subject(subject):  # noqa: E501
    """Finds Notes by subject

     # noqa: E501

    :param subject:
    :type subject: str

    :rtype: List[Note]
    """
    print('finding note by subject..')
    print('calling dispatch request...')

    jsonObject = json.loads(convertVariableToJson(subject,'subject'))
    jsonObject['requestType'] = 'findNotesBySubject'
    return dispatchRequest(jsonObject)


def get_note_by_title(noteTitle):  # noqa: E501
    """Find note by title

    Returns a single note # noqa: E501

    :param noteTitle: title of the note to return
    :type noteTitle: str

    :rtype: Note
    """
    print('finding note by title..')
    print('calling dispatch request...')

    jsonObject = json.loads(convertVariableToJson(noteTitle,'title'))
    jsonObject['requestType'] = 'getNoteByTitle'
    print(jsonObject)
    return dispatchRequest(jsonObject)


def update_note(body):  # noqa: E501
    """Update an existing note

     # noqa: E501

    :param body: Note object that needs to be updated
    :type body: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        body = Note.from_dict(connexion.request.get_json())  # noqa: E501
        print('updating note..')
        print('calling dispatch request...')

        jsonObject = json.loads(convertNoteObjectToJson(body))
        jsonObject['requestType'] = 'updateNote'
        print(jsonObject)
        return dispatchRequest(jsonObject)
