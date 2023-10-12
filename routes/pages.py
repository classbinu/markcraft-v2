from flask import Flask, Blueprint, render_template, request, redirect, url_for, flash
from pymongo import MongoClient
from .api import verify_token
from random import choice, sample
import markdown

pages_bp = Blueprint("pages", __name__)
client = MongoClient("localhost", 27017)
db = client.test

study_set = {
    1: [
        "# 1수준 헤더입니다",
        "## 2수준 헤더입니다",
        "### 3수준 헤더입니다",
        "#### 4수준 헤더입니다",
        "##### 5수준 헤더입니다",
        "###### 6수준 헤더입니다",
    ],
    2: [
        "안녕하세요<br>크래프톤 정글입니다",
        "이곳은 경기대학교입니다<br>언덕이 무척 높습니다",
    ],
    3: ["수평선 위입니다\n***\n수평선 아래입니다"],
    4: [
        "**이 문장은 볼드체입니다**",
        "_이 문장은 이탤릭입니다_",
        "~~이 문장은 취소선입니다~~",
    ],
    5: [">인용입니다"],
    6: ["모듈을 불러오는 예약어는 `import`입니다"],
    7: ["+ 순서가 없는 목록입니다"],
    8: ["1. 순서가 있는 목록입니다"],
    9: ["[Google](https://www.google.com)"],
    10: ["![크래프톤 정글](https://buly.kr/DwAhhgk)"],
}


def millisecondsToMinutesSeconds(milliseconds):
    seconds = int(milliseconds / 1000)
    minutes = seconds // 60
    seconds %= 60
    formattedTime = f"{minutes:02d}:{seconds:02d}"
    return formattedTime


@pages_bp.route("/401error")
def error():
    return render_template("error/Error.html")


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
    question = choice(study_set[chapter_id])
    template_path = f"classroom/chapter{chapter_id}.html"
    html = markdown.markdown(question)
    return render_template(
        template_path, question=question, chapter_id=chapter_id, html=html
    )


@pages_bp.route("/timeattack", methods=["GET"])
def get_timeattack():
    try:
        token = request.cookies.get("access_token")
        if not token:  # 토큰 secret 오류 발행해서 예외 처리로 임시 처리
            flash("로그인이 필요합니다.")
            return redirect(url_for("pages.get_signin"))

        users = verify_token(token)
        user = db.users.find_one({"email": users["email"]})
        myBestTime = int(user["bestTime"])
        formattedMyBestTime = millisecondsToMinutesSeconds(myBestTime)

        topRanker = list(db.users.find().sort("bestTime", 1).limit(1))
        formattedBestTime = millisecondsToMinutesSeconds(topRanker[0]["bestTime"])

        test_set = ["# 헤더1", "## 헤더2", "### 헤더3", "#### 헤더4", "##### 헤더5"]
        questions = sample(test_set, 5)

        # 랭커 가져오기
        rankers = list(db.users.find().sort("bestTime", 1).limit(3))
        # rankers에 있는 회원 수가 3명 미만인 경우 더미 데이터 추가
        while len(rankers) < 3:
            rankers.append({"nickname": "참가자 없음", "bestTime": 5940000})

        for ranker in rankers:
            ranker["bestTime"] = millisecondsToMinutesSeconds(ranker["bestTime"])

        return render_template(
            "timeattack/index.html",
            topRanker=topRanker,
            formattedBestTime=formattedBestTime,
            formattedMyBestTime=formattedMyBestTime,
            questions=questions,
            ranker_1=rankers[0],
            ranker_2=rankers[1],
            ranker_3=rankers[2],
        )
    except Exception as e:
        print(e)
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
