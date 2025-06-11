import pika
import sys

connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
channel = connection.channel()

channel.queue_declare(queue="hello")
message = " ".join(sys.argv[1:]) or "Hello World!"
channel.basic_publish(exchange="", routing_key="hello", body=message)
print(f" [x] Sent {message}")

connection.close()


"""
Forgotten acknowledgment
sudo rabbitmqctl list_queues name messages_ready messages_unacknowledged
sudo rabbitmqctl delete_queue task_queue
"""
