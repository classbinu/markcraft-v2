from flask import Flask, jsonify, make_response, request, Blueprint
from pymongo import MongoClient
from flask_bcrypt import Bcrypt
# from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
import jwt


api_bp = Blueprint('api',__name__)
bcrypt = Bcrypt()
# jwt = JWTManager(app)
SECRET = 'random'
client = MongoClient('localhost', 27017)
db = client.test
collection = db["users"]
collection.create_index([("email",1)], unique=True)
collection.create_index([("nickname",1)], unique=True)


def verify_token(token) :
    try:
        decoded_token = jwt.decode(token, SECRET, algorithms='HS256')
        email = decoded_token['email']
        nickname = decoded_token['nickname']

        # 검증 코드
        
        # raise
        # 
        return {'email':email, 'nickname':nickname}
    except Exception as e :
        if str(e) == '' :
            return ''
        elif str(e) == '' :
            return ''





@api_bp.route('/signin', methods=['POST'])
def signin():
    data = request.get_json()
    try:
        checkUser = db.users.find_one({'email':data['email']})
        if checkUser:
            checkUserPw = checkUser['userpw']
            result = bcrypt.check_password_hash(checkUserPw, data['userpw'])
            if not result:
                raise Exception('PasswordMismatch')
            access_token = jwt.encode({'email':checkUser['email'],"nickname":checkUser["nickname"]}, SECRET, algorithm='HS256')
            # return jsonify({"access_token":access_token, "message":"로그인 성공~"})
            response = make_response(jsonify({'message': '로그인 성공'}))
            response.set_cookie('access_token', access_token, httponly=True)
            return response
        else:
            raise Exception('UserNotFound')

        
    except Exception as e:
        if str(e) == 'PasswordMismatch':
            return '비밀번호가 일치하지 않습니다. (로그인 실패)'
        elif str(e) == 'UserNotFound':
            return '사용자 정보(Email)가 일치하지 않습니다. (로그인 실패)'


@api_bp.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    try:
        db.users.insert_one(
            {
                'email':data["email"], 
                'nickname':data["nickname"], 
                'userpw':bcrypt.generate_password_hash(data['userpw']).decode('utf-8')
            }
        )
        return '회원가입 성공'

    except:
        return '에러 발생'
    


@api_bp.route('/timeattack', methods=['POST'])
def timeattack():
    return jsonify({'result':'hi'})
