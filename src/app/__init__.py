from flask import Flask, request, jsonify
from service.messageService import MessageService

app = Flask(__name__)
app.config.from_pyfile('config.py')

messageService = MessageService()

@app.route('/v1/ds/message', methods=['POST'])
def handle_message():
    message = request.json.get('message')
    result = messageService.process_message(message)
    return jsonify(result)

@app.route("/", methods=['GET'])
def handle_get():
    print("Hello wold!")


if __name__ == "__main__":
    app.run(host="localhost", port=8000, debug=True)