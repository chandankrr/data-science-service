from flask import Flask, request, jsonify, send_from_directory
from kafka import KafkaProducer
import json
from .service.messageService import MessageService
import os
from flask_swagger_ui import get_swaggerui_blueprint

app = Flask(__name__)
app.config.from_pyfile('config.py')

messageService = MessageService()

kafka_host = os.getenv('KAFKA_HOST', 'localhost')
kafka_port = os.getenv('KAFKA_PORT', '9092')
kafka_bootstrap_servers = f"{kafka_host}:{kafka_port}"

producer = KafkaProducer(bootstrap_servers=kafka_bootstrap_servers,
                         value_serializer=lambda v: json.dumps(v).encode('utf-8'))

# Swagger UI configuration
SWAGGER_URL = '/swagger-ui.html'
API_URL = '/static/swagger.json'
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={'app_name': "Swagger UI"}
)
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

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

@app.route('/static/<path:path>')
def static_files(path):
    return send_from_directory('static', path)

if __name__ == "__main__":
    app.run(host="localhost", port=9830, debug=True)