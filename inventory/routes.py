from flask import flash, redirect, render_template, request, url_for

from inventory import app, db
from inventory.form import AssetForm, RegisterForm
from inventory.models import Asset


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/assets/")
def show_assets():
    assets = Asset.query.all()
    return render_template("dashboard.html", assets=assets)


@app.route("/assets/create", methods=("GET", "POST"))
def create_assets():
    form = AssetForm()
    print(form)
    if request.method == "POST":
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
                officer_in_charge=form.officer_in_charge.data.title(),
                officer_contact_info=form.officer_contact_info.data.title(),
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
        print(form.asset_description.data)
        print("Did not validate?")
    return render_template("assets.html", form=form)


@app.route("/account/")
@app.route("/profile/")
def profile():
    return render_template("account.html")


@app.route("/signin/")
@app.route("/SIGNIN/")
@app.route("/LOGIN/")
@app.route("/login/")
def login():
    return render_template("login.html")


@app.route("/register/")
@app.route("/REGISTER/")
@app.route("/SIGNUP/")
@app.route("/signup/")
def register():
    form = RegisterForm()
    return render_template("register.html", form=form)
