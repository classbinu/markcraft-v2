from flask import Flask, Blueprint, render_template

pages_bp = Blueprint('pages',__name__)


@pages_bp.route('/', methods=['GET'])
def get_home():
    return 'This is home!'

@pages_bp.route('/page/signin', methods=['GET'])
def get_signin():
    return 'This is signin!'

@pages_bp.route('/page/signup', methods=['GET'])
def get_signup():
    return 'This is signup!'

@pages_bp.route('/page/lecture', methods=['GET'])
def get_lecture():
    return 'This is lecture!'

@pages_bp.route('/page/note', methods=['GET'])
def get_note():
    return 'This is note!'

@pages_bp.route('/page/timeattack', methods=['GET'])
def get_timeattack():
    return 'This is timeattack!'