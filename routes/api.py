from flask import jsonify, make_response, render_template, request, Blueprint, redirect, url_for, flash
from pymongo import MongoClient
from flask_bcrypt import Bcrypt
import jwt
import datetime
from dotenv import load_dotenv
import os


load_dotenv()
api_bp = Blueprint("api", __name__)
bcrypt = Bcrypt()
SECRET = os.getenv("SECRET")
client = MongoClient(os.getenv("DB"), 27017)
db = client.test
collection = db["users"]
collection.create_index([("email", 1)], unique=True)
collection.create_index([("nickname", 1)], unique=True)
collection.create_index([("bestTime", 1)])


def verify_token(token):
    try:
        # 검증 코드
        # 토큰 존재 유무
        if not token:
            raise Exception("NoTokens")
        decoded_token = jwt.decode(token, SECRET, algorithms="HS256")
        email = decoded_token["email"]
        nickname = decoded_token["nickname"]
        exp = decoded_token["exp"]

        # 토큰 만료 시간
        if exp < int(datetime.datetime.now().timestamp()):
            raise Exception("ExpiredTokens")

        condition = [{"email": email}, {"nickname": nickname}]

        # # 잘못된 토큰. 토큰 값이 db에 없는 email이나 nickname일때
        if not db.users.find_one({"$and": condition}):
            raise Exception("IncorrectTokens")
        # # raise
        # # No Tokens
        # # Expirated Token
        return {"email": email, "nickname": nickname, "exp": exp}

    except Exception as e:
        if str(e) == "NoTokens":
            return "토큰이 존재하지 않습니다."
        elif str(e) == "ExpiredTokens":
            return "만료된 토큰입니다."
        elif str(e) == "IncorrectTokens":
            return "잘못된 토큰입니다."
        else:
            return str(e)


@api_bp.route("/signin", methods=["POST"])
def signin():
    data = request.form
    try:
        checkUser = db.users.find_one({"email": data["email"]})
        if checkUser:
            checkUserPw = checkUser["userpw"]
            result = bcrypt.check_password_hash(checkUserPw, data["userpw"])
            if not result:
                raise Exception("IncorrectPassWord")

            expires = datetime.datetime.utcnow() + datetime.timedelta(hours=2)
            payload = {
                "email": checkUser["email"],
                "nickname": checkUser["nickname"],
                "exp": expires,
            }
            access_token = jwt.encode(payload, SECRET, algorithm="HS256")
            response = make_response(redirect("/"))
            response.set_cookie("access_token", access_token, expires=expires)

            return response

        else:
            raise Exception("UserNotFound")

    except Exception as e:
        if str(e) == "IncorrectPassWord":
            flash("Error: 비밀번호가 옳바르지 않습니다. (로그인 실패)")
            return redirect(url_for("pages.error"))
        elif str(e) == "UserNotFound":
            flash("Error: 사용자 정보(Email)가 일치하지 않습니다. (로그인 실패)")
            return redirect(url_for("pages.error"))
        else:
            return str(e)


@api_bp.route("/signup", methods=["POST"])
def signup():
    data = request.form
    try:
        db.users.insert_one(
            {
                "email": data["email"],
                "nickname": data["nickname"],
                "userpw": bcrypt.generate_password_hash(data["userpw"]).decode("utf-8"),
                "bestTime": 5940000,
                "progress": 0,
            }
        )
        expires = datetime.datetime.utcnow() + datetime.timedelta(hours=2)
        payload = {"email": data["email"], "nickname": data["nickname"], "exp": expires}
        access_token = jwt.encode(payload, SECRET, algorithm="HS256")
        response = make_response(redirect("/"))
        response.set_cookie("access_token", access_token, expires=expires)
        return response

    except Exception as e:
        Error = e.__class__.__name__
        if Error == "DuplicateKeyError":
            flash("Error:이미 존재하는 아아디/닉네임 입니다.")
            return redirect(url_for("pages.get_signup"))
        elif Error == "ConnectionFailure":
            flash("Error: DB Unconneted")
            return redirect(url_for("pages.get_signup"))
        else :
            return redirect(url_for("pages.get_signup"))

@api_bp.route("/timeattack", methods=["POST"])
def timeattack():
    token = request.cookies.get("access_token")
    user = verify_token(token)
    timeScore = request.json.get("myTime")
    user = db.users.find_one({"email": user["email"]})
    if int(user["bestTime"]) > timeScore:
        collection.update_one(
            {"email": user["email"]}, {"$set": {"bestTime": timeScore}}
        )
        return jsonify({"modal_title": "'내 기록 갱신완료!'", "completion_time": timeScore})

    return jsonify({"modal_title": "'기록 갱신 실패!'", "completion_time": timeScore})

@api_bp.route("/progress", methods=["POST"])
def setProgress():
    user = verify_token(request.cookies.get("access_token"))
    try:
        progress = request.json.get('progress')
        if progress is None:
            raise Exception("NoneData")
        db.users.update_one({"email":user["email"],"nickname":user["nickname"]},{"$set":{"progress":progress}})
        return jsonify({"message":"진도 저장 완료!"})

    except Exception as e :
        if str(e) == "NoneData":
            return jsonify({"message":"잘못된 데이터이다."})

    

@api_bp.route("/mypage", methods=["POST"])
def update_nickname():
    user = verify_token(request.cookies.get("access_token"))
    nickname = request.form.get("nickname")
    db.users.update_one({"email":user["email"],"nickname":user["nickname"]},{"$set":{"nickname":nickname}})
    expires = datetime.datetime.utcnow() + datetime.timedelta(hours=2)
    payload = {"email": user["email"], "nickname": nickname, "exp": expires}
    access_token = jwt.encode(payload, SECRET, algorithm="HS256")
    response = make_response(redirect("/"))
    response.set_cookie("access_token", access_token, expires=expires)
    return response