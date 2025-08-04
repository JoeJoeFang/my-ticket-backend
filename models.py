from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import JSON

db = SQLAlchemy()


# This class represents a Host model in the database
class Host(db.Model):
    __tablename__ = "host"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(80), nullable=False)
    companyName = db.Column(db.String(20), nullable=False)
    from_time = db.Column(db.String(10), nullable=True)
    to_time = db.Column(db.String(10), nullable=True)
    datentime = db.Column(db.String(30), nullable=True)
    street = db.Column(db.String(100), nullable=True)
    suburb = db.Column(db.String(100), nullable=True)
    state = db.Column(db.String(100), nullable=True)
    post_code = db.Column(db.String(10), nullable=True)
    description = db.Column(db.String(1000), nullable=True)

# This class represents a Customer model in the database
class Customer(db.Model):
    __tablename__ = "customer"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(160), nullable=False)
    name = db.Column(db.String(20), nullable=False)
    cvc = db.Column(db.String(20), nullable=False)
    duedate = db.Column(db.String(20), nullable=True)
    from_time = db.Column(db.String(10), nullable=True)
    to_time = db.Column(db.String(10), nullable=True)
    datentime = db.Column(db.String(30), nullable=True)
    street = db.Column(db.String(100), nullable=True)
    suburb = db.Column(db.String(100), nullable=True)
    state = db.Column(db.String(100), nullable=True)
    post_code = db.Column(db.String(10), nullable=True)
    cardNumber = db.Column(db.String(100), nullable=True)
    wallet = db.Column(db.Integer, nullable=True)
    order = db.Column(JSON, nullable=True)


# This class represents a Email model in the database
class Email(db.Model):
    __tablename__ = "email"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(80), nullable=False)
    role = db.Column(db.String(20), nullable=False)
    token = db.Column(db.String(50), nullable=False)
    expires = db.Column(db.DateTime, nullable=True)

# This class represents a Events model in the database
class Events(db.Model):
    __tablename__ = "events"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    hostId = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(20), nullable=False)
    address = db.Column(db.String(100), nullable=True)
    price = db.Column(db.Integer, nullable=True)
    organizername = db.Column(db.String(100), nullable=True)
    type = db.Column(db.String(100), nullable=True)
    seats = db.Column(db.String(100), nullable=True)
    duration = db.Column(db.Integer, nullable=True)
    from_time = db.Column(db.String(10), nullable=True)
    to_time = db.Column(db.String(10), nullable=True)
    description = db.Column(db.String(100), nullable=True)
    URL = db.Column(db.String(100), nullable=True)
    thumbnail = db.Column(db.Text, nullable=True)

# This class represents a Order model in the database
class Events_order(db.Model):
    __tablename__ = "events_order"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    eventtitle = db.Column(db.String(20), nullable=False)
    orderdetails = db.Column(JSON, nullable=True)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'))

# This class represents a Comment model in the database
class Comments(db.Model):
    __tablename__ = "comments"
    eventId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    comment = db.Column(JSON, nullable=True)