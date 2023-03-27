from typing import Optional


class Postgres:
    host: Optional[str]
    port: int
    password: str

    def __init__(self, yaml_data):
        self.host = yaml_data.get("host")
        self.port = yaml_data["port"]
        self.password = yaml_data["password"]


class MongoDb:
    host: str
    port: int

    def __init__(self, yaml_data):
        self.host = yaml_data["host"]
        self.port = yaml_data["port"]


class Database:
    postgres: Postgres
    mongo_db: MongoDb

    def __init__(self, yaml_data):
        self.postgres = Postgres(yaml_data["postgres"])
        self.mongo_db = MongoDb(yaml_data["mongo-db"])


class Github:
    is_local: bool

    def __init__(self, yaml_data):
        self.is_local = yaml_data["is-local"]


class Gitlab:
    is_local: bool

    def __init__(self, yaml_data):
        self.is_local = yaml_data["is-local"]


class VcsProvider:
    call_amount_average: Optional[float]
    github: Github
    gitlab: Gitlab

    def __init__(self, yaml_data):
        self.call_amount_average = yaml_data.get("call-amount-average")
        self.github = Github(yaml_data["github"])
        self.gitlab = Gitlab(yaml_data["gitlab"])


class Config:
    database: Database
    vcs_provider: VcsProvider

    def __init__(self, yaml_data):
        self.database = Database(yaml_data["database"])
        self.vcs_provider = VcsProvider(yaml_data["vcs-provider"])
