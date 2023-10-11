from flask import Flask, jsonify, request
from pymongo import MongoClient
from flask_bcrypt import Bcrypt

app = Flask(__name__)
bcrypt = Bcrypt(app)

client = MongoClient('localhost', 27017)
db = client.test
collection = db["users"]
collection.create_index([("email",1)], unique=True)
collection.create_index([("nickname",1)], unique=True)
@app.route('/', methods=['GET'])
def get_home():
    return 'This is home!'

@app.route('/page/signin', methods=['GET'])
def get_signin():
    return 'This is signin!'

@app.route('/page/signup', methods=['GET'])
def get_signup():
    return 'This is signup!'

@app.route('/page/lecture', methods=['GET'])
def get_lecture():
    return 'This is lecture!'

@app.route('/page/note', methods=['GET'])
def get_note():
    return 'This is note!'

@app.route('/page/timeattack', methods=['GET'])
def get_timeattack():
    return 'This is timeattack!'

@app.route('/signin', methods=['POST'])
def signin():
    return 0

@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    db.users.insert_one(
        {
            'email':data["email"], 
            'nickname':data["nickname"], 
            'userpw':bcrypt.generate_password_hash(data['userpw']).decode('utf-8')
        }
    )
    return '회원가입 성공'


@app.route('/timeattack', methods=['POST'])
def timeattack():
    return jsonify({'result':'hi'})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)