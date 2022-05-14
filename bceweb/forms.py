from flask_wtf import FlaskForm
try:  # wtforms 2.x
    from wtforms.fields.html5 import DateField, IntegerField, SelectField
except ImportError:  # wtforms 3.x
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
    qid = SelectField(
        "qid:",
        choices=[(1, "Addr #"), (2, "Addr # Active"), (3, "Utxo #"), (4, "Utxo ∑"), (5, "Vout #"), (6, "Vout ∑")],
        coerce=int
    )
    date0 = DateField("from:")
    date1 = DateField("to:")
