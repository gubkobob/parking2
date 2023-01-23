import random

import factory
import factory.fuzzy as fuzzy

from parking.main.app import db
from parking.main.models import Client, Parking


class ClientFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Client
        sqlalchemy_session = db.session

    name = factory.Faker("first_name")
    surname = factory.Faker("last_name")
    credit_card = factory.LazyAttribute(
        lambda x: random.choice(["1111333355568888", None])
    )
    car_number = fuzzy.FuzzyText(length=8)


class ParkingFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Parking
        sqlalchemy_session = db.session

    address = factory.Faker("address")
    opened = factory.LazyAttribute(lambda x: random.choice([True, False]))
    count_places = factory.LazyAttribute(lambda x: random.randrange(10, 1000))
    count_available_places = factory.LazyAttribute(
        lambda x: random.randrange(0, x.count_places)
    )
