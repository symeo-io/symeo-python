from typing import Optional


class Config:
    database: str

    def __init__(self, yaml_data):
        self.database = yaml_data["database"]
