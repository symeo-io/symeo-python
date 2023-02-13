class MongoDb:
    url: str
    port: int

    def __init__(self, yaml_data):
        self.url = yaml_data["url"]
        self.port = yaml_data["port"]


class Database:
    mongo_db: MongoDb

    def __init__(self, yaml_data):
        self.mongo_db = MongoDb(yaml_data["mongo-db"])


class Github:
    api: str

    def __init__(self, yaml_data):
        self.api = yaml_data["api"]


class Infrastructure:
    name: str
    database: Database
    github: Github

    def __init__(self, yaml_data):
        self.name = yaml_data["name"]
        self.database = Database(yaml_data["database"])
        self.github = Github(yaml_data["github"])


class Config:
    infrastructure: Infrastructure
    application_name: str

    def __init__(self, yaml_data):
        self.infrastructure = Infrastructure(yaml_data["infrastructure"])
        self.application_name = yaml_data["application-name"]
