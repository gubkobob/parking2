from datetime import datetime, timedelta

import pytest
from flask import template_rendered

from parking.main.app import create_app
from parking.main.app import db as _db
from parking.main.models import Client, ClientParking, Parking


@pytest.fixture
def app():
    _app = create_app()
    _app.config["TESTING"] = True
    _app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite://"

    with _app.app_context():
        _db.create_all()

        client1 = Client(
            id=1,
            name="name",
            surname="surname",
            credit_card="1234-5678-1234-9876",
            car_number="o777oo77",
        )
        client2 = Client(id=2, name="name2", surname="surname2", car_number="o777ee77")
        parking1 = Parking(
            id=1,
            opened=True,
            address="Moscow,Tverskaya 1",
            count_places=100,
            count_available_places=50,
        )
        parking2 = Parking(
            id=2,
            opened=False,
            address="Moscow,Tverskaya 3",
            count_places=77,
            count_available_places=55,
        )
        client_parking1 = ClientParking(
            id=1, time_in=datetime.now() - timedelta(hours=2), client_id=1, parking_id=1
        )
        client_parking2 = ClientParking(
            id=2, time_in=datetime.now() + timedelta(hours=1), client_id=2, parking_id=2
        )

        _db.session.add(client1)
        _db.session.add(parking1)
        _db.session.add(client2)
        _db.session.add(parking2)
        _db.session.add(client_parking1)
        _db.session.add(client_parking2)
        _db.session.commit()

        yield _app
        _db.session.close()
        _db.drop_all()


@pytest.fixture
def client(app):
    client = app.test_client()
    yield client


@pytest.fixture
def db(app):
    with app.app_context():
        yield _db
