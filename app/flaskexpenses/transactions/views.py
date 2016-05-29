# -*- coding: utf-8 -*-
"""User views."""
from datetime import datetime

from flask import Blueprint, render_template, redirect
from flask.globals import request
from flask.helpers import flash, url_for

from flaskexpenses.transactions.forms import TransactionForm
from flaskexpenses.transactions.models import Trx
from flaskexpenses.utils import flash_errors


blueprint = Blueprint('transactions', __name__, url_prefix='/transactions', static_folder='../static')


@blueprint.route('/')
def home():
    """List members."""
    return render_template('transactions/home.html')


@blueprint.route('/new', methods=['GET', 'POST'])
def new():
    """Add new Transaction."""
    form = TransactionForm(request.form, csrf_enabled=False)
    if form.validate_on_submit():
#         User.create(username=form.username.data, email=form.email.data, password=form.password.data, active=True)
        t = Trx()
        t.type = form.type.data
        t.amount = form.amount.data
        t.account = form.account.data
        t.created_at = datetime.now()
        t.save()
        
        flash('Thank you for registering. You can now log in.', 'success')
        return redirect(url_for('transactions.home'))
    else:
        flash_errors(form)

    return render_template('transactions/new.html', form=form)


@blueprint.route('/graphs')
def graphs():
    """List members."""
    return render_template('transactions/kibana.html')

