from flask import Flask
from flask_bcrypt import Bcrypt, bcrypt
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.app_context().push()
app.config["SECRET_KEY"] = (
    "\xb1z\x13b\xd9\xcb\xab\xae>\x823\\b\xd6P\xf2\xee\x16\x16\x98s\x13c\xbe"
)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

app.config['OAUTH2_PROVIDERS'] = {
    # Google OAuth 2.0 documentation:
    # https://developers.google.com/identity/protocols/oauth2/web-server#httprest
    'google': {
        'client_id': '1057144427942-i44qpksr1e73bi5ovf46343t03790rnl.apps.googleusercontent.com',
        'client_secret':'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',
        'authorize_url': 'https://accounts.google.com/o/oauth2/auth',
        'token_url': 'https://accounts.google.com/o/oauth2/token',
        'userinfo': {
            'url': 'https://www.googleapis.com/oauth2/v3/userinfo',
            'email': lambda json: json['email'],
        },
        'scopes': ['https://www.googleapis.com/auth/userinfo.email'],
    },
}

from inventory import routes
