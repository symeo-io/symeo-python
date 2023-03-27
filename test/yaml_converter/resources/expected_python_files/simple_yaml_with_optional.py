from typing import Optional


class Database:
    host: Optional[str]
    port: int
    password: str

    def __init__(self, yaml_data):
        self.host = yaml_data.get("host")
        self.port = yaml_data["port"]
        self.password = yaml_data["password"]


class Config:
    database: Database

    def __init__(self, yaml_data):
        self.database = Database(yaml_data["database"])
