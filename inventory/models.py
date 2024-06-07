from inventory import app, db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.Text, nullable=False)
    second_name = db.Column(db.Text, nullable=False)
    email = db.Column(db.Text, unique=True, nullable=False)
    password = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return "<User %r>" % self.first_name


class Asset(db.Model):
    idassets = db.Column(db.Integer, primary_key=True)
    asset_description = db.Column(db.Text, nullable=False)
    room = db.Column(db.Integer, nullable=False)
    serial_number = db.Column(db.Text, nullable=False, unique=True)
    building = db.Column(db.Text, nullable=False)
    product_number = db.Column(db.Text, nullable=False)
    make_model = db.Column(db.Text, nullable=False)
    department = db.Column(db.Text, nullable=False)
    directorate = db.Column(db.Text, nullable=False)
    units = db.Column(db.Text, nullable=False)
    officer_in_charge = db.Column(db.Text, default="N/A")
    state = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return "<User %r>" % self.serial_number
