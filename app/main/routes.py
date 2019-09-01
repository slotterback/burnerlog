from flask import render_template
from flask_login import login_required
from app.main import bp
from app.models import User

@bp.route('/')
@bp.route('/index')
@login_required
def index():
    return render_template('main/index.html')

@bp.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('user.html', user=user)


