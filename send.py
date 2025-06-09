import pika

connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
channel = connection.channel()

channel.queue_declare(queue="hello")
channel.basic_publish(exchange="", routing_key="hello", body="Hello Thurain!")
print(" [x] Sent 'Hello Thurain!'")

connection.close()
