from flask import render_template, url_for

from inventory import app
from inventory.form import AssetForm, RegisterForm


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/assets/")
def show_assets():
    return render_template("dashboard.html")


@app.route("/assets/create")
def create_assets():
    form = AssetForm()
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
