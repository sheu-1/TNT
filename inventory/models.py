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
    def __init__(
        self,
        asset_description,
        financed_by,
        serial_number,
        product_number,
        make_model,
        directorate,
        units,
        department,
        building,
        room,
        officer_in_charge,
        state,
    ):
        self.asset_description = asset_description
        self.financed_by = financed_by
        self.serial_number = serial_number
        self.product_number = product_number
        self.make_model = make_model
        self.directorate = directorate
        self.units = units
        self.department = department
        self.building = building
        self.room = room
        self.officer_in_charge = officer_in_charge
        self.state = state

    idassets = db.Column(db.Integer, primary_key=True)
    asset_description = db.Column(db.Text, nullable=False)
    financed_by = db.Column(db.Text, default="N/A")
    serial_number = db.Column(db.Text, nullable=False, unique=True)
    product_number = db.Column(db.Text, nullable=False)
    make_model = db.Column(db.Text, nullable=False)
    directorate = db.Column(db.Text, nullable=False)
    units = db.Column(db.Text, nullable=False)
    department = db.Column(db.Text, nullable=False)
    building = db.Column(db.Text, nullable=False)
    room = db.Column(db.Integer, nullable=False)
    officer_in_charge = db.Column(db.Text, default="N/A")
    state = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return "<Serial Number %r>" % self.serial_number
