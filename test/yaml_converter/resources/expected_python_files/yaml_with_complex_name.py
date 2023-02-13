class Config:
    database_url: str

    def __init__(self, yaml_data):
        self.database_url = yaml_data["database-url"]
