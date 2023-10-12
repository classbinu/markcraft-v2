from flask import (
    Flask,
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    send_from_directory,
)
from pymongo import MongoClient
from .api import verify_token
from random import choice, sample
import markdown
from dotenv import load_dotenv
import os
import re

load_dotenv()
pages_bp = Blueprint("pages", __name__)
client = MongoClient(os.getenv("LOCALDB"), 27017)
db = client.test
app = Flask(__name__)

study_set = {
    1: [
        "# 1수준 제목입니다",
        "## 2수준 제목입니다",
        "### 3수준 제목입니다",
        "#### 4수준 제목입니다",
        "##### 5수준 제목입니다",
        "###### 6수준 제목입니다",
    ],
    2: ["안녕하세요<br>크래프톤 정글입니다", "이곳은 경기대학교입니다<br>언덕이 무척 높습니다", "독도는<br>우리땅"],
    3: ["수평선 위입니다\r\n***\r\n수평선 아래입니다"],
    4: [
        "**이 텍스트의 스타일은 볼드입니다**",
        "_이 텍스트의 스타일은 이탤릭입니다_",
        "~~이 텍스트의 스타일은 취소선입니다~~",
    ],
    5: [">성장하는 개발자가 되고 싶다면 크래프톤 정글에 합류하세요"],
    6: ["특정 모듈 전체를 가져오는 파이썬 예약어는 `import`입니다"],
    7: [
        "+ 파이썬은 귀도 반 로섬\r\n+ C언어는 데니스 리치\r\n+ 자바스크립트는 브렌든 아이크",
    ],
    8: ["1. 미니 프로젝트\r\n1. 알고리즘\r\n1. 운영체제"],
    9: ["[Google](https://google.com)"],
    10: [
        "![정글](http://15.164.92.132/static/image/jungle.jpeg)",
        "![마크크래프트](http://15.164.92.132/static/image/qr.png)",
    ],
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


# 정적 파일 호스팅(권장 방법 아님)
@app.route("/static/<path:filename>")
def serve_static(filename):
    return send_from_directory("static", filename)


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

        if progress == 10:
            return redirect(url_for("pages.get_graduation"))
        else:
            nextProgress = progress + 1
        return redirect(url_for("pages.get_chapter", chapter_id=nextProgress))
    except:
        return redirect(url_for("pages.get_signin"))


@pages_bp.route("/classroom/chapter/<int:chapter_id>", methods=["GET"])
def get_chapter(chapter_id):
    question = choice(study_set[chapter_id])
    template_path = f"classroom/chapter{chapter_id}.html"
    html = markdown.markdown(question)
    print(question)
    print(html)

    # 챕터9~10 전용 텍스트/url
    text = ""
    url = ""
    # 챕터9(링크), 챕터10(이미지) 힌트 생성
    text_pattern = r"\[(.*?)\]"  # 대괄호 내부 정규식
    url_patter = r"\((.*?)\)"  # 소괄호 내부 정규식
    if chapter_id == 9 or chapter_id == 10:
        text = re.search(text_pattern, question).group(1)
        url = re.search(url_patter, question).group(1)

    return render_template(
        template_path,
        question=question,
        chapter_id=chapter_id,
        html=html,
        text=text,
        url=url,
    )


@pages_bp.route("/classroom/graduation", methods=["GET"])
def get_graduation():
    try:
        token = request.cookies.get("access_token")
        if not token:  # 토큰 secret 오류 발행해서 예외 처리로 임시 처리
            flash("로그인이 필요합니다.")
            return redirect(url_for("pages.get_signin"))
        verify_token(token)["email"]
        return render_template("classroom/graduation.html")
    except:
        return redirect(url_for("pages.get_signin"))


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

        # 임시 테스트 셋, 개행 문자 오류 수정 못할 경우
        # test_set = [
        #     "# 1수준 제목입니다",
        #     "이곳은 경기대학교입니다<br>언덕이 무척 높습니다",
        #     "수평선 위입니다\r\n***\r\n수평선 아래입니다"
        #      "**이 텍스트의 스타일은 볼드입니다**",
        #     "_이 텍스트의 스타일은 이탤릭입니다_",
        #     "~~이 텍스트의 스타일은 취소선입니다~~",
        #     ">성장하는 개발자가 되고 싶다면 크래프톤 정글에 합류하세요",
        #     "특정 모듈 전체를 가져오는 파이썬 예약어는 `import`입니다",
        #     "+ 파이썬은 귀도 반 로섬\r\n+ C언어는 데니스 리치\r\n+ 자바스크립트는 브렌든 아이크",
        #     "1. 미니 프로젝트\r\n1. 알고리즘\r\n1. 운영체제",
        # ]
        test_set = [
            "# 1수준 제목입니다",
            "**이 텍스트의 스타일은 볼드입니다**",
            "_이 텍스트의 스타일은 이탤릭입니다_",
            "~~이 텍스트의 스타일은 취소선입니다~~",
            ">성장하는 개발자가 되고 싶다면 크래프톤 정글에 합류하세요",
            "특정 모듈 전체를 가져오는 파이썬 예약어는 `import`입니다",
        ]
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
