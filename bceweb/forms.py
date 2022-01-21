from flask_wtf import FlaskForm
from wtforms import DateField, IntegerField


class ND0D1Form(FlaskForm):
    """Form for N, Date0, Date1
    :todo: validate (N < ∞, date0 ≤ date1)
    """
    num = IntegerField("Num:")
    date0 = DateField("from:")
    date1 = DateField("to:")
