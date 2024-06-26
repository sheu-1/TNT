from flask_wtf import FlaskForm
from wtforms import (BooleanField, EmailField, PasswordField, SelectField,
                     StringField, SubmitField, ValidationError, validators)
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
    # asset_description = StringField(
    #     "Asset Description", validators=[DataRequired(), Length(min=2, max=19)]
    # )
    asset_description = SelectField(
        "Asset Description",
        choices=[
            ("Monitor", "Monitor"),
            (
                "System Unit(CPU)",
                "System Unit(CPU)",
            ),
            ("Uninterrupted Power Supply(UPS)", "Uninterrupted Power Supply(UPS)"),
            ("Laptop", "Laptop"),
            ("Keyboard", "Keyboard"),
            ("Mouse", "Mouse"),
            ("Printer", "Printer"),
            ("Scanner", "Scanner"),
            ("External Harddrive", "External Hardrive"),
            ("Router", "Router"),
            ("Switch","Switch"),
            ("Mobile Phone","Mobile Phone"),
            ("Desk Phone(VoIp)","Desk Phone(VoIp)"),
            ("Projectors","Projectors"),
            ("Smart Boards","Smart Boards"),
            ("Shredder","Shredder")
        ],
    )
    financed_by = StringField("Financed by/ Source")
    serial_number = StringField(
        "Serial Number", validators=[DataRequired(), Length(min=5, max=20)]
    )
    product_number = StringField(
        "Product Number", validators=[DataRequired(), Length(min=3, max=20)]
    )
    make_model = StringField("Make Model", validators=[DataRequired()])
    # directorate = StringField("Directorate", validators=[DataRequired()])
    directorate = SelectField(
        "Directorate",
        choices=[
            ("Accounting Services", "Directorate of Accounting Services"),
            (
                "Budget, Fiscal and Economic Affairs",
                "Directorate of Budget, Fiscal and Economic Affairs",
            ),
            ("Public Investment", "Directorate of Public Investment"),
            ("Public Debt Management", "Directorate of Public Debt Management"),
            ("Administrative Services", "Directorate of Administrative Services"),
            ("Public Private Partnership", "Directorate of Public Private Patnership"),
        ],
    )
    units = StringField("Units", validators=[DataRequired()])
    building = StringField("Building", validators=[DataRequired()])
    room = StringField("Room", validators=[DataRequired()])
    officer_allocated = StringField(
        "Officer Allocated Names", validators=[Length(min=2, max=20)]
    )
    officer_contact_info = StringField("Officer Allocated Work ID / National ID")
    state = StringField("Condition", validators=[DataRequired()])
    # language = SelectField(
    #     "Programming Language",
    #     choices=[("cpp", "C++"), ("py", "Python"), ("text", "Plain Text")],
    # )

    def validate_serial_number(self, serial_number):
        serial_number = Asset.query.filter_by(serial_number=serial_number.data).first()
        if serial_number:
            raise ValidationError(
                "The serial number you entered is already in use. Please verify your entry or check the existing records to avoid duplicates."
            )


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember = BooleanField("Remember Me")
    submit = SubmitField("Login")


class UpdateAccountForm(RegisterForm):
    first_name = StringField(
        "First Name", validators=[DataRequired(), Length(min=2, max=12)]
    )
    second_name = StringField(
        "Second Name", validators=[DataRequired(), Length(min=2, max=12)]
    )
    email = EmailField("Email", validators=[Email(), DataRequired()])
    new_password = PasswordField("New Password", validators=[Length(min=6)])
    confirm_new_password = PasswordField(
        "Confirm New Password", validators=[Length(min=6), EqualTo("new_password")]
    )
    submit = SubmitField("Update your Account")


class DeleteAccountForm(FlaskForm):
    password = PasswordField("Password:", validators=[DataRequired(), Length(min=6)])
    submit = SubmitField("Proceed to delete")
