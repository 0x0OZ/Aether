from pymongo import MongoClient


class Monate:
    client = MongoClient("mongodb://localhost:27017/")

    def __init__(self, db_name, peers_collection_name, logs_collection_name) -> None:
        self.database = self.client[db_name]
        self.peers_collection = self.database[peers_collection_name]
        self.logs_collection = self.database[logs_collection_name]

        pass

    def insert_logs(self, logs) -> None:
        if type(logs) == type([]):
            self.logs_collection.insert_many(logs)
        else:
            self.logs_collection.insert_one(logs)

        print(f"Inserted Logs into: {self.logs_collection.name}")
        pass

    def insert_peers(self, peers) -> None:
        print("peers:",peers)
        print(type(peers))
        if type(peers) == type([]):
            self.peers_collection.insert_many(peers)
        else:
            self.peers_collection.insert_one(peers)
        print(f"Inserted Peers Into: {self.peers_collection.name}")
        pass

    def read_logs(self):
        logs = self.logs_collection.find()
        print(logs)
        return logs

    def read_peers(self):
        peers = self.peers_collection.find()
        print(peers)
        return peers
