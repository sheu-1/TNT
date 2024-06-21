from flask_wtf import FlaskForm
from wtforms import (
    BooleanField,
    EmailField,
    PasswordField,
    StringField,
    SubmitField,
    ValidationError,
    validators,
)
from wtforms.validators import DataRequired, Email, EqualTo, Length

from inventory.models import Asset, User


class RegisterForm(FlaskForm):
    first_name = StringField(validators=[DataRequired(), Length(min=2, max=12)])
    second_name = StringField(validators=[DataRequired(), Length(min=2, max=12)])
    email = EmailField(validators=[Email(), DataRequired()])
    password = PasswordField(validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField(
        validators=[DataRequired(), EqualTo("password"), Length(min=6)]
    )
    submit = SubmitField()


class AssetForm(FlaskForm):
    asset_description = StringField(validators=[DataRequired(), Length(min=2, max=19)])
    financed_by = StringField()
    serial_number = StringField(validators=[DataRequired(), Length(min=5, max=20)])
    product_number = StringField(validators=[DataRequired(), Length(min=3, max=20)])
    make_model = StringField(validators=[DataRequired()])
    directorate = StringField(validators=[DataRequired()])
    units = StringField(validators=[DataRequired()])
    building = StringField(validators=[DataRequired()])
    room = StringField(validators=[DataRequired()])
    officer_in_charge = StringField(validators=[Length(min=2, max=20)])
    officer_contact_info = StringField()
    state = StringField(validators=[DataRequired()])

    def validate_serial_number(self, serial_number):
        serial_number = Asset.query.filter_by(serial_number=serial_number.data).first()
        if serial_number:
            raise ValidationError("Serial Number already exists")

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')