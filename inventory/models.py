from flask_login import UserMixin

# from itsdangerous import URLSafeTimedSerializer as Serializer
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

from inventory import app, db, login_manager


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.Text, nullable=False)
    email = db.Column(db.Text, unique=True, nullable=False)
    password = db.Column(db.Text, nullable=False)
    is_oauth_user = db.Column(db.Boolean, default=False)

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(app.config["SECRET_KEY"], expires_sec)
        return s.dumps({"user_id": self.id}).decode("utf-8")

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config["SECRET_KEY"])
        try:
            user_id = s.loads(token)["user_id"]
        except:
            return None
        return User.query.get(user_id)

    def remove(self):
        db.session.delete(self)

    def get_id(self):
        return self.id

    def __repr__(self):
        return "<User %r>" % self.full_name


class Asset(db.Model):
    idassets = db.Column(db.Integer, primary_key=True)
    asset_description = db.Column(db.Text, nullable=False)
    financed_by = db.Column(db.Text, default="N/A")
    serial_number = db.Column(db.Text, nullable=False, unique=True)
    product_number = db.Column(db.Text, nullable=False)
    make_model = db.Column(db.Text, nullable=False)
    directorate = db.Column(db.Text, nullable=False)
    units = db.Column(db.Text, nullable=False)
    building = db.Column(db.Text, nullable=False)
    room = db.Column(db.Integer, nullable=False)
    officer_allocated = db.Column(db.Text, default="N/A")
    officer_contact_info = db.Column(db.Text, default="0")
    state = db.Column(db.Text, nullable=False)
    recorded_by = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f"Asset('{self.asset_description}','{self.financed_by}','{self.serial_number}','{self.product_number}','{self.make_model}','{self.directorate}','{self.units}','{self.building}','{self.room}','{self.officer_allocated}','{self.officer_contact_info}','{self.state}')"
