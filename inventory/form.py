from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import (BooleanField, EmailField, IntegerField, PasswordField,
                     SelectField, StringField, SubmitField, ValidationError)
from wtforms.validators import DataRequired, Email, EqualTo, Length

from inventory.models import Asset, User


class RegisterForm(FlaskForm):
    full_name = StringField(validators=[DataRequired(), Length(min=6, max=12)])
    email = EmailField(validators=[Email(), DataRequired()])
    password = PasswordField(validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField(
        validators=[DataRequired(), EqualTo("password"), Length(min=6)]
    )
    submit = SubmitField()

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("Email already exists.")


class AssetForm(FlaskForm):
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
            ("Switch", "Switch"),
            ("Mobile Phone", "Mobile Phone"),
            ("Desk Phone(VoIp)", "Desk Phone(VoIp)"),
            ("Projectors", "Projectors"),
            ("Smart Boards", "Smart Boards"),
            ("Shredder", "Shredder"),
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
        validators=[DataRequired()],
    )
    units = SelectField("Units / Departments", choices=[], validators=[DataRequired()])
    building = StringField("Building", validators=[DataRequired()])

    room = StringField("Room", validators=[DataRequired()])
    officer_allocated = StringField(
        "Officer Allocated Names", validators=[Length(min=2, max=20)]
    )
    officer_contact_info = IntegerField("Officer Allocated Work ID / National ID")
    state = StringField("Condition", validators=[DataRequired()])

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


class UpdateAccountForm(FlaskForm):
    full_name = StringField(
        "Full Names:", validators=[DataRequired(), Length(min=6, max=12)]
    )
    email = EmailField("Email:", validators=[Email(), DataRequired()])
    submit = SubmitField("Update your Account Info")

    def validate_email(self, email):
        if current_user.email != email.data:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError("Email already exists.")


class UpdatePasswordForm(FlaskForm):
    new_password = PasswordField("New Password:", validators=[Length(min=6)])
    confirm_new_password = PasswordField(
        "Confirm New Password:", validators=[Length(min=6), EqualTo("new_password")]
    )
    submit = SubmitField("Update your Password")


class UpdateAssetForm(FlaskForm):
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
            ("Switch", "Switch"),
            ("Mobile Phone", "Mobile Phone"),
            ("Desk Phone(VoIp)", "Desk Phone(VoIp)"),
            ("Projectors", "Projectors"),
            ("Smart Boards", "Smart Boards"),
            ("Shredder", "Shredder"),
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
        validators=[DataRequired()],
    )
    units = SelectField("Units / Departments", choices=[], validators=[DataRequired()])
    building = StringField("Building", validators=[DataRequired()])

    room = StringField("Room", validators=[DataRequired()])
    officer_allocated = StringField(
        "Officer Allocated Names", validators=[Length(min=2, max=20)]
    )
    officer_contact_info = IntegerField("Officer Allocated Work ID / National ID")
    state = StringField("Condition", validators=[DataRequired()])

class DeleteAccountForm(FlaskForm):
    password = PasswordField("Password:", validators=[DataRequired(), Length(min=6)])
    submit = SubmitField("Proceed to delete")
