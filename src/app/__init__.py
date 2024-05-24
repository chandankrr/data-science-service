from flask import Flask, request, jsonify
from kafka import KafkaProducer
import json
from service.messageService import MessageService

app = Flask(__name__)
app.config.from_pyfile('config.py')

messageService = MessageService()
producer = KafkaProducer(bootstrap_servers=['localhost:9092'],
                         value_serializer=lambda v: json.dumps(v).encode('utf-8'))

@app.route('/v1/ds/message', methods=['POST'])
def handle_message():
    message = request.json.get('message')
    result = messageService.process_message(message)
    serialized_result = result.json()

    # send the serialized result to kafka topic
    producer.send('expense_service', serialized_result)
    
    return jsonify(result)

@app.route("/", methods=['GET'])
def handle_get():
    return "Hello wold!"


if __name__ == "__main__":
    app.run(host="localhost", port=8000, debug=True)