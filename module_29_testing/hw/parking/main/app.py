from datetime import datetime
from typing import List

from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///prod.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)

    from .models import Client, ClientParking, Parking, ParkingLog

    @app.before_first_request
    def before_request_func():
        # db.drop_all()
        db.create_all()

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db.session.remove()

    @app.route("/test_route")
    def math_route():
        """Тестовый роут для расчета степени"""
        number = int(request.args.get("number", 0))
        result = number**2
        return jsonify(result)

    @app.route("/clients", methods=["POST"])
    def create_client_handler():
        """Создание нового клиента"""
        name = request.form.get("name", type=str)
        surname = request.form.get("surname", type=str)
        credit_card = request.form.get("credit_card", type=str)
        car_number = request.form.get("car_number", type=str)

        new_client = Client(
            name=name, surname=surname, credit_card=credit_card, car_number=car_number
        )

        db.session.add(new_client)
        db.session.commit()

        return "", 201

    @app.route("/parkings", methods=["POST"])
    def create_parking_handler():
        """Создание новой парковки"""
        address = request.form.get("address", type=str)
        opened = request.form.get("opened", type=bool)
        count_places = request.form.get("count_places", type=int)
        count_available_places = request.form.get("count_available_places", type=int)

        new_parking = Parking(
            address=address,
            opened=opened,
            count_places=count_places,
            count_available_places=count_available_places,
        )

        db.session.add(new_parking)
        db.session.commit()

        return "", 201

    @app.route("/clients", methods=["GET"])
    def get_clients_handler():
        """Получение клиентов"""
        clients: List[Client] = db.session.query(Client).all()
        clients_list = [u.to_json() for u in clients]
        return jsonify(clients_list), 200

    @app.route("/parkings", methods=["GET"])
    def get_parkings_handler():
        """Получение парковок"""
        parkings: List[Parking] = db.session.query(Parking).all()
        parkings_list = [u.to_json() for u in parkings]
        return jsonify(parkings_list), 200

    @app.route("/clients/<int:client_id>", methods=["GET"])
    def get_client_handler(client_id: int):
        """Получение клиента по ид"""
        client: Client = db.session.query(Client).get(client_id)
        return jsonify(client.to_json()), 200

    @app.route("/client_parkings", methods=["POST"])
    def post_client_parking():
        """Въезд клиента на парковку"""
        client_id = request.form.get("client_id", type=int)
        parking_id = request.form.get("parking_id", type=int)
        client = db.session.query(Client).get(client_id)
        parking = db.session.query(Parking).get(parking_id)
        if (
            client
            and parking
            and parking.opened
            and (parking.count_available_places > 0)
        ):
            new_client_parking = ClientParking(
                client_id=client_id, parking_id=parking_id, time_in=datetime.now()
            )

            try:
                db.session.add(new_client_parking)
                parking.count_available_places -= 1
                db.session.commit()
            except:
                return "Ошибка: уже на парковке", 404
            return "", 201
        else:
            return "Невозможно заехать на парковку", 404

    @app.route("/client_parkings", methods=["DELETE"])
    def delete_client_parking():
        """Выезд клиента с парковки"""
        client_id = request.form.get("client_id", type=int)
        parking_id = request.form.get("parking_id", type=int)
        client_parking = (
            db.session.query(ClientParking)
            .filter(
                ClientParking.client_id == client_id,
                ClientParking.parking_id == parking_id,
            )
            .one_or_none()
        )
        if client_parking:
            if not client_parking.client.credit_card:
                return "Нечем оплачивать", 404
            if client_parking.time_in > datetime.now():
                return "Нельзя выехать раньше, чем заехать", 404

            client_parking.parking.count_available_places += 1
            client_parking_log = ParkingLog(
                client_id=client_parking.client_id,
                parking_id=client_parking.parking_id,
                time_in=client_parking.time_in,
                time_out=datetime.now(),
            )
            db.session.add(client_parking_log)
            db.session.query(ClientParking).filter(
                ClientParking.id == client_parking.id
            ).delete()
            db.session.commit()
            return "", 201
        else:
            return "Нет такой машины на такой парковке", 404

    return app
