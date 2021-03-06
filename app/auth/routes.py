from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user
from werkzeug.urls import url_parse
from app import db
from app.auth import bp
from app.auth.forms import LogInForm, RegistrationForm, \
    ResetPasswordRequestForm, ResetPasswordForm, UserUpdateName, \
    UserUpdateEmail, UserUpdateActive
from app.models import User
from app.auth.email import send_password_reset_email


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LogInForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('auth.login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('main.index')
        return redirect(next_page)
    return render_template('auth/login.html', title='Sign In', form=form)


@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))


@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', title='Register',
                           form=form)


@bp.route('/user_update', methods=['GET', 'POST'])
def user_update():
    form = UserUpdateName()
    if form.validate_on_submit():
        if current_user.check_password(form.password.data):
            current_user.setName(form.username.data)
            db.session.commit()
        else:
            flash('Password is Invalid')
        return redirect(url_for('main.user',username=current_user.getName()))
    return render_template('auth/user_update.html', title='Update Username',
                           form=form)

 
@bp.route('/email_update', methods=['GET', 'POST'])
def email_update():
    form = UserUpdateEmail()
    if form.validate_on_submit():
        if current_user.check_password(form.password.data):
            current_user.setEmail(form.email.data)
            db.session.commit()
        else:
            flash('Password is Invalid')
        return redirect(url_for('main.user', username=current_user.getName()))
    return render_template('auth/email_update.html', 
                           title='Update Email Address',
                           form=form)


@bp.route('/active_update', methods=['GET', 'POST'])
def active_update():
    form = UserUpdateActive()
    if form.validate_on_submit():
        if current_user.check_password(form.password.data):
            if form.active.data:
                current_user.activateUser()
            else:
                current_user.deactivateUser()
            db.session.commit()
        else:
            flash('Password is Invalid')
        return redirect(url_for('main.user', username=current_user.getName()))
    return render_template('auth/active_update.html',
                           title='Update Active Status',
                           form = form)


@bp.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash('Check your email for the instructions to reset your password')
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password_request.html',
                           title='Reset Password', form=form)


@bp.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('main.index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash(_('Your password has been reset.'))
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password.html', form=form)
