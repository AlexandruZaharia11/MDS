from pymongo import MongoClient


class DatabaseConnection:

    instance = None

    def __init__(self):
        self.client = MongoClient()
        self.database = self.client.MeteoStation

    @staticmethod
    def get_instance():
        if DatabaseConnection.instance is None:
            instance = DatabaseConnection()

        return instance


