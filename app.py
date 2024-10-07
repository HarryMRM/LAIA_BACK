from flask import Flask
from flask_cors import CORS
from routes.text_to_speech import text_to_speech_route

app = Flask(__name__)
CORS(app)
app.register_blueprint(text_to_speech_route)

if __name__ == '__main__':
    app.run(debug=True)
