import json
from datetime import datetime, timedelta

import pytest

from parking.main.models import Client, ClientParking, Parking


def test_math_route(client) -> None:
    resp = client.get("/test_route?number=8")
    data = json.loads(resp.data.decode())
    assert data == 64


def test_client(client) -> None:
    resp = client.get("/clients/1")
    assert resp.status_code == 200
    assert resp.json == {
        "id": 1,
        "name": "name",
        "surname": "surname",
        "credit_card": "1234-5678-1234-9876",
        "car_number": "o777oo77",
    }


def test_create_client(client) -> None:
    client_data = {
        "name": "Александр",
        "surname": "Белов",
        "credit_card": "1111-2222-3334-4444",
        "car_number": "e323ee77",
    }
    resp = client.post("/clients", data=client_data)

    assert resp.status_code == 201


def test_create_parking(client) -> None:
    parking_data = {
        "opened": True,
        "address": "Moscow,Lubyanka 22",
        "count_places": 40,
        "count_available_places": 10,
    }
    resp = client.post("/parkings", data=parking_data)

    assert resp.status_code == 201


@pytest.mark.parking
def test_create_client_parking(client, db) -> None:

    client_parking_data = {
        "time_in": datetime.now() - timedelta(hours=2),
        "client_id": 2,
        "parking_id": 1,
    }
    resp = client.post("/client_parkings", data=client_parking_data)

    client_parking_data2 = {
        "time_in": datetime.now() - timedelta(hours=3),
        "client_id": 1,
        "parking_id": 2,
    }
    resp2 = client.post("/client_parkings", data=client_parking_data2)

    db.session.commit()

    places = (
        db.session.query(Parking.count_available_places)
        .filter(Parking.id == 1)
        .scalar()
    )

    assert places == 49
    assert resp.status_code == 201
    assert resp2.status_code == 404
    assert resp2.data.decode() == "Невозможно заехать на парковку"


@pytest.mark.parking
def test_delete_client_parking(client, db) -> None:

    client_parking_data1 = {"client_id": 1, "parking_id": 1}
    resp1 = client.delete("/client_parkings", data=client_parking_data1)

    client_parking_data2 = {"client_id": 2, "parking_id": 2}
    resp2 = client.delete("/client_parkings", data=client_parking_data2)

    places = (
        db.session.query(Parking.count_available_places)
        .filter(Parking.id == 1)
        .scalar()
    )

    assert resp1.status_code == 201
    assert resp2.status_code == 404
    assert (
        resp2.data.decode() == "Нечем оплачивать"
        or "Нельзя выехать раньше, чем заехать"
    )
    assert places == 51


def test_app_config(app):
    assert not app.config["DEBUG"]
    assert app.config["TESTING"]
    assert app.config["SQLALCHEMY_DATABASE_URI"] == "sqlite://"


@pytest.mark.parametrize(
    "route", ["/test_route?number=8", "/clients/1", "/clients", "/parkings"]
)
def test_route_status(client, route):
    rv = client.get(route)
    assert rv.status_code == 200
