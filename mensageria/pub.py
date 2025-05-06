import pika
import os

def open_connection():
    # Get RabbitMQ connection details from environment variables
    rabbitmq_host = os.getenv("RABBITMQ_HOST", "rabbitmq-service")
    rabbitmq_user = os.getenv("RABBITMQ_USER", "guest")
    rabbitmq_pass = os.getenv("RABBITMQ_PASS", "guest")
    
    # Configura as credenciais e os parâmetros de conexão
    credentials = pika.PlainCredentials(rabbitmq_user, rabbitmq_pass)
    parameters = pika.ConnectionParameters(rabbitmq_host,
                                           5672,
                                           '/',
                                           credentials)
    # Abre a conexão e cria um canal
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    
    return connection, channel

def close_connection(connection):
    connection.close()


def publish_message(queue_name, message):

    connection, channel = open_connection()

    # Declare a fila (caso ainda não exista)
    channel.queue_declare(queue=queue_name)

    # Publica a mensagem na fila
    channel.basic_publish(exchange='', routing_key=queue_name, body=message.encode())
    print(f"[Publisher] Enviado: {message}")

    close_connection(connection)
