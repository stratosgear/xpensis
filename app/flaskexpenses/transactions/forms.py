# -*- coding: utf-8 -*-
"""User forms."""
from flask_wtf import Form
from wtforms import  StringField, DateTimeField
from wtforms.fields.core import DecimalField, SelectField
from wtforms.fields.simple import TextAreaField
from wtforms.validators import DataRequired, Length
from wtforms.widgets.core import HTMLString, html_params, TextArea


class TransactionForm(Form):
    """Transaction form."""

    type = SelectField(
        'Transaction Type',
        choices=[('expense', 'Expense'), ('Income', 'Income')]
    )
    account = SelectField(
        'Account',
        choices=[('Stratos Cash', 'Stratos Cash'), ('Arzu Cash', 'Arzu Cash'), ('text', 'Plain Text')]
    )
    amount = DecimalField('Amount', places=2,
                        validators=[DataRequired(), ])
    
    # The date format has to mimic the moment.js format set in:
    # templates/transactions/new.html
    trx_date = DateTimeField('Transaction Date', format="%A, %B %d %Y, %H:%M")

    def __init__(self, *args, **kwargs):
        """Create instance."""
        super(TransactionForm, self).__init__(*args, **kwargs)

    def validate(self):
        """Validate the form."""
        initial_validation = super(TransactionForm, self).validate()
        if not initial_validation:
            return False

        return True

class BulkImportForm(Form):
    """Transaction form."""

    data = TextAreaField()
    
    def __init__(self, *args, **kwargs):
        """Create instance."""
        super(BulkImportForm, self).__init__(*args, **kwargs)

    def validate(self):
        """Validate the form."""
        initial_validation = super(BulkImportForm, self).validate()
        if not initial_validation:
            return False

        return True
