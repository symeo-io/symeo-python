class Database:
    url: str

    def __init__(self, yaml_data):
        self.url = yaml_data["url"]


class Conf:
    database: Database

    def __init__(self, yaml_data):
        self.database = Database(yaml_data["database"])