from pymongo import MongoClient


class Monate:

    def __init__(
        self,
        db,
        db_name,
        peers_collection_name,
        public_peers_collection_name,
        logs_collection_name,
    ) -> None:
        self.client = MongoClient(db)
        self.database = self.client[db_name]
        self.peers_collection = self.database[peers_collection_name]
        self.logs_collection = self.database[logs_collection_name]
        self.public_peers_collection = self.database[public_peers_collection_name]
        pass

    def insert_logs(self, logs) -> None:
        if not logs:
            return
        if type(logs) == type([]):
            self.logs_collection.insert_many(logs)
        else:
            self.logs_collection.insert_one(logs)

        print(f"Inserted Logs into: {self.logs_collection.name}")
        pass

    def insert_public_peers(self, public_peers) -> None:
        if not public_peers:
            return
        if type(public_peers) == type([]):
            self.public_peers_collection.insert_many(public_peers)
        else:
            self.public_peers_collection.insert_one(public_peers)

        print(f"Inserted Public Nodes into: {self.public_peers_collection.name}")
        pass

    def insert_peers(self, peers) -> None:
        if not peers:
            return
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

    def read_public_peers(self):
        return
