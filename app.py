from flask import Flask
from routes.pages import pages_bp
from routes.api import api_bp

app = Flask(__name__)

app.register_blueprint(pages_bp)
app.register_blueprint(api_bp)

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)