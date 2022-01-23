from flask_wtf import FlaskForm
try:  # 2.x
    from wtforms.fields.html5 import DateField, IntegerField
except ImportError:  # 3.x
    from wtforms import DateField, IntegerField


class ND0D1Form(FlaskForm):
    """Form for N, Date0, Date1
    :todo: validate (N < ∞, date0 ≤ date1)
    """
    num = IntegerField("Num:")
    date0 = DateField("from:")
    date1 = DateField("to:")


class ND1Form(FlaskForm):
    """Form for N, Date"""
    num = IntegerField("Sat.:")
    date1 = DateField("Date:")
