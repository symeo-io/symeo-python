class Conf:
    database: int
    name: str

    def __init__(self, yaml_data):
        self.database = yaml_data["database"]
        self.name = yaml_data["name"]
