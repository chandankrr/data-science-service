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

    if result is not None:
        serialized_result = result.serialize()
        producer.send('expense_service', serialized_result)
        return jsonify(serialized_result)
    else:
        return jsonify({'error': 'Invalid message format'}), 400


@app.route("/", methods=['GET'])
def handle_get():
    return "Hello world!"

if __name__ == "__main__":
    app.run(host="localhost", port=9830, debug=True)