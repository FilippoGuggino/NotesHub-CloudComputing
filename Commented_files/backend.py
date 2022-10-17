import pika
from mongoBackend import handle_request
from ZooClient import ZooClient

def consume() :

    print("[x] Trying to connect to RabbitMQ...")
    
    zk = ZooClient("172.16.1.191:2181, 172.16.2.40:2181")
    rabbitUser, rabbitPsw = zk.getRabbitCredentials()
    rabbitIP, rabbitPort = zk.getRabbitAddress()
    

    # Connect to RabbitMQ
    credentials = pika.PlainCredentials(rabbitUser, rabbitPsw)

    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
                    rabbitIP,
                    rabbitPort,
                    '/',
                    credentials
        )
    )
    channel = connection.channel()

    print("[x] Backend is now connected to RabbitMQ")

    #declare the queue  
    queue_name = zk.getQueueName()
    channel.queue_declare(queue_name)

    #To not lose any REST, We ACK it at the end of the handler
    channel.basic_consume(
    	#auto_ack=false for Remote Procedure Call
        queue=queue_name, on_message_callback=handleREST, auto_ack=False)
    channel.start_consuming()

def handleREST(ch, method, props, body):
    print("Request received. Handling it...")
    print("Request: "+body.decode("utf-8"))
    #create request for mongodb
    response = handle_request(body.decode("utf-8"))
    print("Response: " + str(response))

    ch.basic_publish(exchange='',
    				#props.reply_to = name of temporary queue
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(correlation_id = \
                        props.correlation_id),
                     body=str(response))
    ch.basic_ack(delivery_tag=method.delivery_tag)

    print("Response sent back.")


consume()
