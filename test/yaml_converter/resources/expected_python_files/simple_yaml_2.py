class Conf:
    database: int

    def __init__(self, yaml_data):
        self.database = yaml_data["database"]
