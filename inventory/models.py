from flask_login import UserMixin

from inventory import db, login_manager


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.Text, nullable=False)
    email = db.Column(db.Text, unique=True, nullable=False)
    password = db.Column(db.Text, nullable=False)

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
