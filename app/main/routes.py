from datetime import datetime
from flask import render_template, flash, redirect, url_for, request
from flask_login import login_required, current_user
from app import db
from app.main import bp
from app.main.forms import ReportForm, CustomerForm
from app.models import User, Customer, Report

@bp.route('/')
@bp.route('/index')
@login_required
def index():
    reports = Report.query.filter_by(user_id=current_user.id)
    users = User.query.all()
    customers = Customer.query.all()
    return render_template('main/index.html',
                           reports=reports, 
                           users=users,
                           customers=customers)


@bp.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('user.html', user=user)


@bp.route('/customer/<int:id>')
@login_required
def customer(id):
    customer = Customer.query.filter_by(id=id).first_or_404()
    return render_template('main/customer.html', customer=customer)


#todo: figure out how to pass the current customer to the route.
@bp.route('/update_customer/<int:id>', methods=['GET','POST'])
@login_required
def update_customer(id):
    customer = Customer.query.filter_by(id=id).first_or_404()
    form = CustomerForm()
    if request.method == 'GET':
        form.name.data = customer.getName()
        form.notes.data = customer.getNotes()
    if form.validate_on_submit():
        customer.setName(form.name.data)
        customer.setNotes(form.notes.data)
        db.session.commit()
        return redirect(url_for('main.index'))
    return render_template('main/update_customer.html', 
                           customer=customer,
                           form=form)


@bp.route('/create_report', methods=['GET', 'POST'])
@login_required
def create_report():
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
    return render_template('main/create_report.html', 
                           title='Create Report',
                           form=form)


@bp.route('/create_customer', methods=['GET', 'POST'])
@login_required
def create_customer():
    form = CustomerForm()
    if form.validate_on_submit():
        #todo: check for uniqueness
        customer = Customer()
        customer.setName(form.name.data)
        customer.setNotes(form.notes.data)
        db.session.add(customer)
        db.session.commit()
        return redirect(url_for('main.index'))
    return render_template('main/create_customer.html',
                           title='Create New Customer',
                           form=form)


@bp.route('/report/<int:id>')
@login_required
def report(id):
    report = Report.query.filter_by(id=id).first_or_404()
    return render_template('main/report.html', report = report)


@bp.route('/update_report/<int:id>', methods=['GET', 'POST'])
@login_required
def update_report(id):
    report = Report.query.filter_by(id=id).first_or_404()
    form = ReportForm()
    if request.method == 'GET':
        form.summary.data = report.getSummary()
        form.action.data = report.getAction()
        form.recommendation.data = report.getRecommendation()
    if form.validate_on_submit():
        report.setSummary(form.summary.data)
        report.setAction(form.action.data)
        report.setRecommendation(form.recommendation.data)
        db.session.commit()
        return redirect(url_for('main.index'))
    return render_template('main/update_report.html', 
                           title='Update Report',
                           report = report,
                           form=form)


