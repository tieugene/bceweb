from flask_wtf import FlaskForm
from wtforms import DateField, IntegerField, SelectField


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
    qid = SelectField("qid:", choices=[(1, "Addr_Num"), (2, "Addr_Num_Active"), (3, "Utxo_Num"), (4, "Utxo_Sum")], coerce=int)
    date0 = DateField("from:")
    date1 = DateField("to:")
