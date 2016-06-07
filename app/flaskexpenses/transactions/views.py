# -*- coding: utf-8 -*-
"""User views."""
import StringIO
import csv
from datetime import datetime

from elasticsearch.client import Elasticsearch
from elasticsearch_dsl.query import Q
from elasticsearch_dsl.search import Search
from flask import Blueprint, render_template, redirect
from flask.globals import request
from flask.helpers import flash, url_for

from flaskexpenses.transactions.forms import TransactionForm, BulkImportForm
from flaskexpenses.transactions.models import Trx
from flaskexpenses.transactions.utils import find_oldest_trx_date_and_sum, \
    get_total_balance, get_totals_per_account_type
from flaskexpenses.utils import flash_errors


blueprint = Blueprint('transactions', __name__, url_prefix='/transactions', static_folder='../static')


@blueprint.route('/')
def dashboard():
    """List members."""
    

    total_balance = get_total_balance()
    total_cash, total_cc, total_bank = get_totals_per_account_type()
  
    return render_template('transactions/dashboard.html',
                           total_balance=total_balance,
                           total_cash=total_cash,
                           total_cc=total_cc,
                           total_bank=total_bank)


@blueprint.route('/new', methods=['GET', 'POST'])
def new():
    """Add new Transaction."""
    form = TransactionForm(request.form, csrf_enabled=False)
    if form.validate_on_submit():
        t = Trx()
        t.type = form.type.data
        t.amount = form.amount.data
        t.account = form.account.data
        t.trx_date = form.trx_date.data
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

@blueprint.route('/import', methods=['GET', 'POST'])
def bulk_import():
    form = BulkImportForm(request.form, csrf_enabled=False)
    if form.validate_on_submit():
        _bulk_import(form.data.data)
        
        flash('Your data has been imported', 'success')
        return redirect(url_for('transactions.home'))
    else:
        flash_errors(form)

    return render_template('transactions/import.html', form=form)

def _bulk_import(data):
    print "Bulk importing"
    f = StringIO.StringIO(data)
    reader = csv.reader(f, delimiter=',')
    now = datetime.now()
    
    for row in reader:
        
        trx = Trx()
        
        trx.created_date = now
        
        trx.trx_date = row[0]
        
        trx.type = row[1]
        
        trx.amount = row[2]
        
        if row[3]:
            trx.tags.append(row[3])
            
        if row[4]:
            trx.tags.append(row[4])
            
        trx.description = row[5]
        
        trx.payee = row[6]
        
        trx.account = row[7]
        
        trx.account_type = row[8]
        
        trx.save()
        
        print '\t'.join(row)
