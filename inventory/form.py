from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, StringField, SubmitField, validators
from wtforms.validators import DataRequired, Email, EqualTo, Length


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
    serial_number = StringField(validators=[DataRequired()])
    product_number = StringField(validators=[DataRequired()])
    make_model = StringField(validators=[DataRequired()])
    directorate = StringField()
    units = StringField()
    department = StringField(validators=[DataRequired()])
    building = StringField(validators=[DataRequired()])
    room = StringField(validators=[DataRequired()])
    officer_in_charge = StringField()
    condition = StringField(validators=[DataRequired()])
