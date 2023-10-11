from flask import Flask, Blueprint, render_template

pages_bp = Blueprint('pages',__name__)


@pages_bp.route('/', methods=['GET'])
def get_home():
    return render_template('index.html')

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
