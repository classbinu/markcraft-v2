from flask import Flask, Blueprint, render_template, request, redirect, url_for, flash
from pymongo import MongoClient
from .api import verify_token

pages_bp = Blueprint("pages", __name__)
client = MongoClient("mongodb://markcraft:1234@localhost", 27017)
db = client.test


def millisecondsToMinutesSeconds(milliseconds):
    seconds = int(milliseconds / 1000)
    minutes = seconds // 60
    seconds %= 60
    formattedTime = f"{minutes:02d}:{seconds:02d}"
    return formattedTime


@pages_bp.route("/", methods=["GET"])
def get_home():
    token = request.cookies.get("access_token")
    isLoggedIn = False
    if token:
        isLoggedIn = True

    rankers = list(db.users.find().sort("bestTime", 1).limit(3))
    # rankers에 있는 회원 수가 3명 미만인 경우 더미 데이터 추가
    while len(rankers) < 3:
        rankers.append({"nickname": "참가자 없음", "bestTime": 5940000})

    for ranker in rankers:
        ranker["bestTime"] = millisecondsToMinutesSeconds(ranker["bestTime"])
    return render_template(
        "index.html",
        ranker_1=rankers[0],
        ranker_2=rankers[1],
        ranker_3=rankers[2],
        isLoggedIn=isLoggedIn,
    )


@pages_bp.route("/signin", methods=["GET"])
def get_signin():
    return render_template("auth/signin.html")


@pages_bp.route("/signup", methods=["GET"])
def get_signup():
    return render_template("auth/signup.html")


@pages_bp.route("/classroom", methods=["GET"])
def get_classroom():
    try:
        token = request.cookies.get("access_token")
        if not token:  # 토큰 secret 오류 발행해서 예외 처리로 임시 처리
            flash("로그인이 필요합니다.")
            return redirect(url_for("pages.get_signin"))

        email = verify_token(token)["email"]
        user = db.users.find_one({"email": email})
        progress = user["progress"]
        nextProgress = 10 if progress == 10 else progress + 1
        return redirect(url_for("pages.get_chapter", chapter_id=nextProgress))
    except:
        return redirect(url_for("pages.get_signin"))


@pages_bp.route("/classroom/chapter/<int:chapter_id>", methods=["GET"])
def get_chapter(chapter_id):
    template_path = f"classroom/chapter{chapter_id}.html"
    return render_template(template_path)


@pages_bp.route("/timeattack", methods=["GET"])
def get_timeattack():
    try:
        token = request.cookies.get("access_token")
        if not token:  # 토큰 secret 오류 발행해서 예외 처리로 임시 처리
            flash("로그인이 필요합니다.")
            return redirect(url_for("pages.get_signin"))

        topRanker = list(db.users.find().sort("bestTime", 1).limit(1))
        formattedBestTime = millisecondsToMinutesSeconds(topRanker[0]["bestTime"])
        return render_template(
            "timeattack/index.html",
            topRanker=topRanker,
            formattedBestTime=formattedBestTime,
        )
    except:
        return redirect(url_for("pages.get_signin"))


@pages_bp.route("/note", methods=["GET"])
def get_note():
    try:
        token = request.cookies.get("access_token")
        if not token:  # 토큰 secret 오류 발행해서 예외 처리로 임시 처리
            flash("로그인이 필요합니다.")
            return redirect(url_for("pages.get_signin"))
        return render_template("note/index.html")
    except:
        return redirect(url_for("pages.get_signin"))
