from typing import Any, Dict

from .app import db


class Client(db.Model):
    __tablename__ = "clients"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    surname = db.Column(db.String(50), nullable=False)
    credit_card = db.Column(db.String(50), nullable=True)
    car_number = db.Column(db.String(10), nullable=True)

    def __repr__(self):
        return f"Клиент {self.name} {self.surname}"

    def to_json(self) -> Dict[str, Any]:
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Parking(db.Model):
    __tablename__ = "parkings"

    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(100), nullable=False)
    opened = db.Column(db.Boolean)
    count_places = db.Column(db.Integer, nullable=False)
    count_available_places = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Парковка, адрес: {self.title}"

    def to_json(self) -> Dict[str, Any]:
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class ParkingLog(db.Model):
    __tablename__ = "parking_log"

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    client_id = db.Column(db.Integer, db.ForeignKey("clients.id"), nullable=False)
    parking_id = db.Column(db.Integer, db.ForeignKey("parkings.id"), nullable=False)
    time_in = db.Column(db.DateTime, nullable=False)
    time_out = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return f"Parking on {self.address}"

    def to_json(self) -> Dict[str, Any]:
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class ClientParking(db.Model):
    __tablename__ = "clientparkings"
    __table_args__ = (
        db.UniqueConstraint("client_id", "parking_id", name="_unique_client_parking"),
    )

    id = db.Column(db.Integer, primary_key=True)
    time_in = db.Column(db.DateTime)
    time_out = db.Column(db.DateTime)
    client = db.relationship("Client", backref="parkings")
    parking = db.relationship("Parking", backref="clients")
    client_id = db.Column(db.Integer, db.ForeignKey("clients.id"))
    parking_id = db.Column(db.Integer, db.ForeignKey("parkings.id"))

    def __repr__(self):
        return f"Машина клиента {self.client} на парковке  {self.parking}"

    def to_json(self) -> Dict[str, Any]:
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
