from typing import Optional


class Database:
    host: str
    port: int

    def __init__(self, yaml_data):
        self.host = yaml_data["host"]
        self.port = yaml_data["port"]


class Client:
    premium: bool
    average_cart_price: float

    def __init__(self, yaml_data):
        self.premium = yaml_data["premium"]
        self.average_cart_price = yaml_data["average-cart-price"]


class Config:
    database: Database
    client: Client

    def __init__(self, yaml_data):
        self.database = Database(yaml_data["database"])
        self.client = Client(yaml_data["client"])
