from flask_wtf import FlaskForm
try:  # wtforms 2.x
    from wtforms.fields.html5 import IntegerField, DateField
except ImportError:  # wtforms 3.x
    from wtforms import IntegerField, DateField
from wtforms import BooleanField, SelectField, RadioField

QID_LIST = ((1, "Addr, #"), (2, "Addr, # Active"), (3, "Utxo, #"), (4, "Utxo, ₿"), (5, "Vout, #"), (6, "Vout, ₿"))
RID_LIST = ((1, "≤.001"), (2, "001….01"), (3, ".01….1"), (4, ".1…1"), (5, "1…10"), (6, "10…100"), (7, "100…1k"), (8, "1k…10k"), (9, "10k…100k"), (10, "100k…1m"), (11, ">1m"))


class ND0D1Form(FlaskForm):
    """Form for N, Date0, Date1
    :todo: validate (N < ∞, date0 ≤ date1)
    """
    num = IntegerField("Num:")
    date0 = DateField("from:")
    date1 = DateField("to:")


class ND1Form(FlaskForm):
    """Form for N, Date"""
    num = IntegerField("BTC.:")
    date1 = DateField("Date:")


class Q1ATableForm(FlaskForm):
    qid = RadioField("qid:", choices=QID_LIST, coerce=int)
    date0 = DateField("from:")
    date1 = DateField("to:")


class Q1A2DDatesForm(FlaskForm):
    qid = SelectField("qid:", choices=QID_LIST, coerce=int)
    rid = SelectField("rid:", choices=RID_LIST, coerce=int)
    date0 = DateField("from:")
    date1 = DateField("to:")
    percent = BooleanField("%")


class Q1A2DRIDForm(FlaskForm):
    qid = SelectField("qid:", choices=QID_LIST, coerce=int)
    date0 = DateField("date:")
    percent = BooleanField("%")
