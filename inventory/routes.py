from flask import flash, redirect, render_template, request, url_for

from inventory import app, db, bcrypt
from inventory.form import AssetForm, RegisterForm, LoginForm
from inventory.models import Asset, User
from flask_login import login_user, current_user, logout_user, login_required


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


@app.route("/signin/", methods=("GET", "POST"))
@app.route("/SIGNIN/", methods=("GET", "POST"))
@app.route("/LOGIN/", methods=("GET", "POST"))
@app.route("/login/", methods=("GET", "POST"))
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            print(user)
            print(bcrypt.check_password_hash(user.password, form.password.data))
            if user and bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                return redirect(url_for('index'))
            else:
                flash('Login unsuccessful. Please check email and password', 'danger')
    return render_template("login.html", title=login, form=form)


@app.route("/register/", methods=['POST', 'GET'])
@app.route("/REGISTER/", methods=['GET', 'POST'])
@app.route("/SIGNUP/", methods=['GET', 'POST'])
@app.route("/signup/", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegisterForm()
    print(form)
    if request.method == "POST":
        if form.validate_on_submit():
            first_name=form.first_name.data
            second_name=form.second_name.data
            email=form.email.data
            password=form.password.data
             
            hashed_password = bcrypt.generate_password_hash(password)
            user = User(
               first_name=first_name,
               second_name= second_name,
               email=email,
               password=hashed_password
               )
            
            db.session.add(user)
            db.session.commit()
            flash(f" {form.first_name.data}has  been successfully registered", "success")
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
            
    return render_template("register.html", form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('index'))