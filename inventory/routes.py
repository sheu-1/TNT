from flask import flash, jsonify, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user

from inventory import app, bcrypt, db
from inventory.form import (
    AssetForm,
    DeleteAccountForm,
    LoginForm,
    RegisterForm,
    UpdateAccountForm,
)
from inventory.models import Asset, User


@app.route("/")
def index():
    return render_template("index.html")


# def get_total_asset_count():
#     assets = Asset.query.all()
#     return str(len(assets))


@app.route("/assets/")
@login_required
def show_assets():
    assets = Asset.query.all()
    return render_template("dashboard.html", assets=assets)


unit_options = {
    "Accounting Services": [
        "Government Accounting",
        "National Sub-County Treasuries",
        "IFMIS",
        "Audit Department",
    ],
    "Budget, Fiscal and Economic Affairs": [
        "Budget Department",
        "Macro and Fiscal Affairs",
        "Financial and Sectoral Affairs",
        "Inter Government Fiscal Relations",
        "Public Procurement",
    ],
    "Public Investment": [
        "Government Public Investment and Public Enterprises",
        "National Assets and Liability Management",
        "Pensions Department",
    ],
    "Public Debt Management": [
        "Resource Mobilization (Front Office)",
        "Debt Policy Strategy and Risk Management (Middle Office)",
        "Debt Recording and Settlement (Back Office)",
    ],
    "Administrative Services": ["Admin", "HRM", "ICT", "Finance", "Accounts", "SCM"],
    "Public Private Partnership": [
        "CPPMU",
        "Legal",
        "Public Communications",
        "Internal Audit and Risk Assesment",
    ],
}


@app.route("/assets/create", methods=("GET", "POST"))
@login_required
def create_assets():
    form = AssetForm()
    print(form)
    if request.method == "POST":
        # set unit choices before submit
        directorate = form.directorate.data
        form.units.choices = [
            (unit, unit) for unit in unit_options.get(directorate, [])
        ]
        if form.validate_on_submit():
            asset = Asset(
                asset_description=form.asset_description.data.title(),
                financed_by=form.financed_by.data.title(),
                serial_number=form.serial_number.data.upper(),
                product_number=form.product_number.data.upper(),
                make_model=form.make_model.data.upper(),
                directorate=form.directorate.data.title(),
                units=form.units.data.title(),
                building=form.building.data.title(),
                room=form.room.data.title(),
                officer_allocated=form.officer_allocated.data.title(),
                officer_contact_info=form.officer_contact_info.data,
                state=form.state.data.capitalize(),
            )
            db.session.add(asset)
            db.session.commit()
            flash(f"Asset {form.asset_description.data} successfully added!", "success")
            return redirect(url_for("create_assets"))
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    print(
                        f"Error in {getattr(form, field).label.text}: {error}", "error"
                    )
    else:
        # Pre-fill items based on default category
        default_directorate = form.directorate.data or "Accounting Services"
        form.units.choices = [
            (unit, unit) for unit in unit_options[default_directorate]
        ]
        print(form.asset_description.data)
        print("Did not validate?")
    return render_template("assets.html", form=form)


@app.route("/get_units", methods=["POST"])
def get_units():
    directorate = request.json["directorate"]
    units = unit_options.get(directorate, [])
    return jsonify(units)


@app.route("/account/", methods=("GET", "POST"))
@app.route("/profile/", methods=("GET", "POST"))
@login_required
def profile():
    form = UpdateAccountForm()
    print(current_user.full_name)
    if request.method == "GET":
        form.full_name.data = current_user.full_name
        form.email.data = current_user.email
        print(request.method)
    if request.method == "POST" and form.validate_on_submit():
        print(request.method)
        if (
            current_user.full_name == form.full_name.data
            and current_user.email == form.email.data
        ):
            redirect(url_for("profile"))
        else:
            print(current_user.full_name)
            current_user.full_name = form.full_name.data
            current_user.email = form.email.data
            if form.new_password.data:
                hashed_password = bcrypt.generate_password_hash(form.new_password.data)
                current_user.password = hashed_password
            else:
                current_user.password = current_user.password
            db.session.commit()
            flash("Your account has been updated successfully!", "success")
            return redirect(url_for("show_assets"))

    return render_template("account.html", form=form)


@app.route("/signin/", methods=("GET", "POST"))
@app.route("/SIGNIN/", methods=("GET", "POST"))
@app.route("/LOGIN/", methods=("GET", "POST"))
@app.route("/login/", methods=("GET", "POST"))
def login():
    if current_user.is_authenticated:
        return redirect(url_for("show_assets"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for("show_assets"))
        else:
            flash("Login unsuccessful. Please check email and password", "danger")
    return render_template("login_user.html", title=login, form=form)


@app.route("/register/", methods=["POST", "GET"])
@app.route("/REGISTER/", methods=["GET", "POST"])
@app.route("/SIGNUP/", methods=["GET", "POST"])
@app.route("/signup/", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = RegisterForm()
    print(form)
    if request.method == "POST":
        if form.validate_on_submit():
            full_name = form.full_name.data.title()
            email = form.email.data
            password = form.password.data

            hashed_password = bcrypt.generate_password_hash(password)
            user = User(
                full_name=full_name,
                email=email,
                password=hashed_password,
            )

            db.session.add(user)
            db.session.commit()
            flash(
                f" {form.full_name.data} you have been successfully registered. Log in to proceed.",
                "success",
            )
            return redirect(url_for("login"))
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    print(
                        f"Error in {getattr(form, field).label.text}: {error}", "error"
                    )
    else:
        print(form.email.data)
        print("Did not validate?")

    return render_template("register_user.html", form=form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))


@app.route("/account/delete", methods=("GET", "POST"))
@app.route("/profile/delete", methods=("GET", "POST"))
@login_required
def delete_account():
    form = DeleteAccountForm()
    if form.validate_on_submit():
        if request.method == "POST" and bcrypt.check_password_hash(
            current_user.password, form.password.data
        ):
            current_user.remove()
            db.session.commit()
            flash("You no longer exist :)")
            return redirect(url_for("index"))
        else:
            flash("Incorrect password!", "danger")
    return render_template("confirm_delete.html", form=form)


@app.errorhandler(404)
def error_404(error):
    return render_template("404.html")


@app.errorhandler(403)
def error_403(error):
    return render_template("403.html")


@app.errorhandler(500)
def error_500(error):
    return render_template("500.html")
