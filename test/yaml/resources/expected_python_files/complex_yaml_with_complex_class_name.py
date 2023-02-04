class Conf:
    class Infrastructure:
        class Database:
            class MongoDb:
                url: str
                port: int

            mongo_db: MongoDb

        database: Database

        class Github:
            api: str

        github: Github

    infrastructure: Infrastructure
