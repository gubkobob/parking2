from parking.main.models import Client, Parking

from .factories import ClientFactory, ParkingFactory


def test_create_client(client, db):
    client_data = ClientFactory()
    db.session.commit()

    assert client_data.id is not None
    assert len(db.session.query(Client).all()) == 3


def test_create_parking(client, db):
    parking_data = ParkingFactory()
    db.session.commit()

    assert parking_data.id is not None
    assert len(db.session.query(Parking).all()) == 3
