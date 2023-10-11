from flask import jsonify, make_response, request, Blueprint
from pymongo import MongoClient
from flask_bcrypt import Bcrypt
# from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
import jwt
import datetime


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
        # 검증 코드
        # 토큰 존재 유무
        if not token :
            raise Exception("NoTokens")
        decoded_token = jwt.decode(token, SECRET, algorithms='HS256')
        email = decoded_token["email"]
        nickname = decoded_token["nickname"]
        exp  = decoded_token["exp"]
        
        # 토큰 만료 시간
        if exp < int(datetime.datetime.now().timestamp()) :
            raise Exception("ExpiredTokens")
        
        condition = [{"email":email},{"nickname":nickname}]

        # # 잘못된 토큰. 토큰 값이 db에 없는 email이나 nickname일때
        # # if not db.users.find_one({"$and":condition}) :
        if not db.users.find_one({"$and":condition}):
            raise Exception("IncorrectTokens")
        # # raise
        # # No Tokens
        # # Expirated Token
        return {'email':email, 'nickname':nickname, 'exp':exp}
        
    except Exception as e :
        if str(e) == 'NoTokens' :
            return '토큰이 존재하지 않습니다.'
        elif str(e) == 'ExpiredTokens' :
            return '만료된 토큰입니다.'
        elif str(e) == 'IncorrectTokens':
            return '잘못된 토큰입니다.'
        else :
            return str(e)





@api_bp.route('/signin', methods=['POST'])
def signin():
    data = request.form
    try:
        checkUser = db.users.find_one({'email':data['email']})
        if checkUser:
            checkUserPw = checkUser['userpw']
            result = bcrypt.check_password_hash(checkUserPw, data['userpw'])
            if not result:
                raise Exception('IncorrectPassWord')

            payload = {
                "email":checkUser["email"],
                "nickname":checkUser["nickname"], 
                "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=10)
            }

            access_token = jwt.encode(payload, SECRET, algorithm='HS256')
            response = make_response(jsonify({'message': '로그인 성공'}))
            response.set_cookie('access_token', access_token, httponly=True)

            return response

        else:
            raise Exception('UserNotFound')

        
    except Exception as e:
        if str(e) == 'IncorrectPassWord':
            return '비밀번호가 일치하지 않습니다. (로그인 실패)'
        elif str(e) == 'UserNotFound':
            return '사용자 정보(Email)가 일치하지 않습니다. (로그인 실패)'


@api_bp.route('/signup', methods=['POST'])
def signup():
    data = request.form
    try:
        db.users.insert_one(
            {
                'email':data["email"], 
                'nickname':data["nickname"], 
                'userpw':bcrypt.generate_password_hash(data['userpw']).decode('utf-8')
            }
        )
        return '회원가입 성공'

    except Exception as e:
        return str(e)
    


@api_bp.route('/timeattack', methods=['POST'])
def timeattack():
    token = request.cookies.get("access_token")
    users = verify_token(token)
    timeScore = request.get_json().values()
    # db.users.insert_one({"tie"})
    print(users)
    return jsonify(users)
