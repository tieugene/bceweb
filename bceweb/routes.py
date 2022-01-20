from flask import Blueprint, render_template, session, redirect, request, url_for

bp = Blueprint('bceweb', __name__)


@bp.route('/', methods=['GET'])
def index():
    return render_template('index.html')
