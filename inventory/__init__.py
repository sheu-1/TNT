from flask import Flask
from flask_bcrypt import Bcrypt, bcrypt
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.app_context().push()
app.config["SECRET_KEY"] = (
    "\xb1z\x13b\xd9\xcb\xab\xae>\x823\\b\xd6P\xf2\xee\x16\x16\x98s\x13c\xbe"
)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)


from inventory import routes
