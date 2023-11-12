from flask import Flask
from routes.pages import pages_bp
from routes.api import api_bp
from dotenv import load_dotenv
import os

load_dotenv()
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.register_blueprint(pages_bp)
app.register_blueprint(api_bp)

if __name__ == '__main__':
    app.run('0.0.0.0', port=4999, debug=False)