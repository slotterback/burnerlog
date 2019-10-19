from datetime import datetime
from flask import render_template, flash, redirect, url_for
from flask_login import login_required, current_user
from app import db
from app.main import bp
from app.main.forms import ReportForm
from app.models import User, Customer, Report

@bp.route('/')
@bp.route('/index')
@login_required
def index():
    reports = Report.query.filter_by(user_id=current_user.id)
    return render_template('main/index.html', reports=reports)

@bp.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('user.html', user=user)

@bp.route('/customer/<customer_name>')
@login_required
def customer(customer_name):
    customer = Customer.query.filter_by(customer_name=customer_name).first_or_404()
    return render_template('main/customer.html', customer=customer)

@bp.route('/write_report', methods=['GET', 'POST'])
@login_required
def write_report():
    form = ReportForm()
    if form.validate_on_submit():
        report = Report(author=current_user, 
                        customer=Customer.query.first_or_404(),
                        summary=form.summary.data,
                        action=form.action.data,
                        recommendation = form.recommendation.data)
        db.session.add(report)
        db.session.commit()
        flash('Your report has been recorded!')
        return redirect(url_for('auth.login'))
    return render_template('main/report.html', title='Write Report',
                           form=form)

