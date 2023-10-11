from flask import Flask, Blueprint, render_template, request
from pymongo import MongoClient

pages_bp = Blueprint('pages',__name__)
client = MongoClient('localhost', 27017)
db = client.test

def millisecondsToMinutesSeconds(milliseconds):
    seconds = int(milliseconds / 1000)
    minutes = seconds // 60
    seconds %= 60
    formattedTime = f"{minutes:02d}:{seconds:02d}"
    return formattedTime

@pages_bp.route('/', methods=['GET'])
def get_home():
    token = request.cookies.get("access_token")
    isLoggedIn = False
    if token:
        isLoggedIn = True

    rankers = list(db.users.find().sort("bestTime", 1).limit(3))
    try:
        ranker_1 = rankers[0]
        ranker_2 = rankers[1]
        ranker_3 = rankers[2]

        ranker_1['bestTime'] = millisecondsToMinutesSeconds(ranker_1['bestTime'])
        ranker_2['bestTime'] = millisecondsToMinutesSeconds(ranker_2['bestTime'])
        ranker_3['bestTime'] = millisecondsToMinutesSeconds(ranker_3['bestTime'])
    except StopIteration:
        pass
    return render_template('index.html', ranker_1=ranker_1, ranker_2=ranker_2, ranker_3=ranker_3, isLoggedIn=isLoggedIn)

@pages_bp.route('/signin', methods=['GET'])
def get_signin():
    return render_template('auth/signin.html')

@pages_bp.route('/signup', methods=['GET'])
def get_signup():
    return render_template('auth/signup.html')

@pages_bp.route('/classroom', methods=['GET'])
def get_classroom():
    return render_template('classroom/index.html')

@pages_bp.route('/classroom/chapter/<int:chapter_id>', methods=['GET'])
def get_chapter(chapter_id):
    template_path = f'classroom/chapter{chapter_id}.html'
    return render_template(template_path)

@pages_bp.route('/timeattack', methods=['GET'])
def get_timeattack():
    return render_template('timeattack/index.html')

@pages_bp.route('/note', methods=['GET'])
def get_note():
   return render_template('note/index.html')
