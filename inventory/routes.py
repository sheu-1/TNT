import random
import secrets
import string
from urllib.parse import urlencode

import requests
from flask import (abort, current_app, flash, jsonify, redirect,
                   render_template, request, session, url_for)
from flask_login import current_user, login_required, login_user, logout_user

from inventory import app, bcrypt, db
from inventory.form import (AssetForm, DeleteAccountForm, LoginForm,
                            RegisterForm, UpdateAccountForm, UpdateAssetForm,
                            UpdatePasswordForm)
from inventory.models import Asset, User

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


@app.route("/")
def index():
    assets = Asset.query.all()
    return render_template("index.html", assets=assets)


@app.route("/asset/edit/<int:asset_id>", methods=("GET", "POST"))
def edit_asset(asset_id):
    form = UpdateAssetForm()
    asset = Asset.query.get_or_404(asset_id)
    current_serial = asset.serial_number
    if request.method == "GET":
        form.asset_description.data = asset.asset_description
        form.financed_by.data = asset.financed_by
        form.serial_number.data = asset.serial_number
        form.product_number.data = asset.product_number
        form.make_model.data = asset.make_model
        form.directorate.data = asset.directorate

               # Set units choices based on the current directorate
        form.units.choices = [(unit, unit) for unit in unit_options.get(asset.directorate, [])]
        form.units.data = asset.units  # Set the current unit

        form.building.data = asset.building
        form.room.data = asset.room
        form.officer_allocated.data = asset.officer_allocated
        form.officer_contact_info.data = asset.officer_contact_info
        form.state.data = asset.state
    if request.method == "POST":
        directorate = form.directorate.data
        form.units.choices = [
            (unit,unit) for unit in unit_options.get(directorate, [])
        ]
        if  form.validate_on_submit():
            if (asset.asset_description == form.asset_description.data and
            asset.financed_by == form.financed_by.data and
            asset.serial_number == form.serial_number.data and
            asset.product_number == form.product_number.data and
            asset.make_model == form.make_model.data and
            asset.directorate == form.directorate.data and
            asset.units == form.units.data and
            asset.building == form.building.data and
            asset.room == form.room.data and
            asset.officer_allocated == form.officer_allocated.data and
            asset.officer_contact_info == form.officer_contact_info.data and
            asset.state == form.state.data):
                return redirect(url_for('edit_asset',asset_id=asset.idassets))

            else:
                directorate = form.directorate.data
                form.units.choices = [
                    (unit, unit) for unit in unit_options.get(directorate, [])
                ]
                asset.asset_description = form.asset_description.data
                asset.financed_by = form.financed_by.data
                asset.serial_number = form.serial_number.data
                asset.product_number = form.product_number.data
                asset.make_model = form.make_model.data
                asset.directorate = form.directorate.data
                asset.units = form.units.data
                asset.building = form.building.data
                asset.room = form.room.data
                asset.officer_allocated = form.officer_allocated.data
                asset.officer_contact_info = form.officer_contact_info.data
                asset.state = form.state.data

                db.session.commit()
                flash(f"Asset {asset.asset_description} successfully updated!", "success")
                return redirect(url_for('edit_asset', asset_id=asset.idassets))
    return render_template("edit_asset.html", form=form, asset=asset)


@app.route("/asset/delete/<int:asset_id>", methods=("GET", "POST"))
def delete_asset(asset_id):
    asset = Asset.query.get_or_404(asset_id)
    db.session.delete(asset)
    db.session.commit()
    flash("Asset Successfully deleted", "success")
    return redirect(url_for("index"))

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


@app.route("/account/", methods=["GET", "POST"])
@app.route("/profile/", methods=["GET", "POST"])
@login_required
def profile():
    form = UpdateAccountForm()
    password_form = UpdatePasswordForm()
    if request.method == "GET":
        form.full_name.data = current_user.full_name
        form.email.data = current_user.email
    if form.validate_on_submit():
        if (
            current_user.full_name == form.full_name.data
            and current_user.email == form.email.data
        ):
            redirect(url_for("profile"))
        else:
            print(current_user.full_name)
            current_user.full_name = form.full_name.data.title()
            current_user.email = form.email.data.lower()
            db.session.commit()
            print("Hurrah")
            flash("Your Account Info has been updated successfully!", "success")
            return redirect(url_for("profile"))
    if password_form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(password_form.new_password.data)
        current_user.password = hashed_password
        db.session.commit()
        flash("Your Password has been updated successfully!", "success")
        return redirect(url_for("profile"))
    return render_template("account.html", form=form, password_form=password_form)


@app.route("/signin/", methods=("GET", "POST"))
@app.route("/SIGNIN/", methods=("GET", "POST"))
@app.route("/LOGIN/", methods=("GET", "POST"))
@app.route("/login/", methods=("GET", "POST"))
def login():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            flash("Welcome back", "success")
            return redirect(url_for("index"))
        else:
            flash(
                "Login unsuccessful. Please check if your Email and Password is correct and try again!",
                "danger",
            )
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
            email = form.email.data.lower()
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
            flash("You no longer exist :)", "success")
            return redirect(url_for("index"))
        else:
            flash("Incorrect password!", "danger")
    return render_template("confirm_delete.html", form=form)


@app.route("/authorize/<provider>")
def oauth2_authorize(provider):
    if not current_user.is_anonymous:
        return redirect(url_for("index"))

    provider_data = current_app.config["OAUTH2_PROVIDERS"].get(provider)
    if provider_data is None:
        abort(404)

    # generate a random string for the state parameter
    session["oauth2_state"] = secrets.token_urlsafe(16)

    # create a query string with all the OAuth2 parameters
    qs = urlencode(
        {
            "client_id": provider_data["client_id"],
            "redirect_uri": url_for(
                "oauth2_callback", provider=provider, _external=True
            ),
            "response_type": "code",
            "scope": " ".join(provider_data["scopes"]),
            "state": session["oauth2_state"],
        }
    )

    # redirect the user to the OAuth2 provider authorization URL
    return redirect(provider_data["authorize_url"] + "?" + qs)


@app.route("/callback/<provider>")
def oauth2_callback(provider):
    if not current_user.is_anonymous:
        return redirect(url_for("index"))

    provider_data = current_app.config["OAUTH2_PROVIDERS"].get(provider)
    if provider_data is None:
        abort(404)

    # if there was an authentication error, flash the error messages and exit
    if "error" in request.args:
        for k, v in request.args.items():
            if k.startswith("error"):
                flash(f"{k}: {v}")
        return redirect(url_for("index"))

    # make sure that the state parameter matches the one we created in the
    # authorization request
    if request.args["state"] != session.get("oauth2_state"):
        abort(401)

    # make sure that the authorization code is present
    if "code" not in request.args:
        abort(401)

    # exchange the authorization code for an access token
    response = requests.post(
        provider_data["token_url"],
        data={
            "client_id": provider_data["client_id"],
            "client_secret": provider_data["client_secret"],
            "code": request.args["code"],
            "grant_type": "authorization_code",
            "redirect_uri": url_for(
                "oauth2_callback", provider=provider, _external=True
            ),
        },
        headers={"Accept": "application/json"},
    )
    if response.status_code != 200:
        abort(401)
    oauth2_token = response.json().get("access_token")
    if not oauth2_token:
        abort(401)

    # use the access token to get the user's email address
    response = requests.get(
        provider_data["userinfo"]["url"],
        headers={
            "Authorization": "Bearer " + oauth2_token,
            "Accept": "application/json",
        },
    )
    if response.status_code != 200:
        abort(401)
    email = provider_data["userinfo"]["email"](response.json())

    # find or create the user in the database
    user = db.session.scalar(db.select(User).where(User.email == email))
    if user is None:
        # Generate a random password
        characters = string.ascii_letters + string.digits
        password = "".join(random.choices(characters, k=20))
        hashed_password = bcrypt.generate_password_hash(password)
        user = User(
            email=email, full_name=email.split("@")[0], password=hashed_password
        )
        db.session.add(user)
        db.session.commit()

    # log the user in
    login_user(user)
    return redirect(url_for("index"))


@app.errorhandler(404)
def error_404(error):
    return render_template("404.html")


@app.errorhandler(403)
def error_403(error):
    return render_template("403.html")


@app.errorhandler(500)
def error_500(error):
    return render_template("500.html")
