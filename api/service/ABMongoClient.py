from pymongo import MongoClient

import datetime


class ABMongoClient:

    def __init__(self, host, port):
        self.client = MongoClient(host, port)
        self.db = self.client.alabaster

    def add_registry(self, registry):
        doc = registry.to_dict()
        doc['inUTC'] = datetime.datetime.utcnow()
        doc['version'] = 1
        registries = self.db.registries
        return registries.insert_one(registry).inserted_id

    def add_user(self, user):
        doc = user.to_dict()
        if self.get_user(doc["username"]):
            raise ValueError("Username " + doc["username"] + " already used.")
        doc['inUTC'] = datetime.datetime.utcnow()
        doc['version'] = 1
        users = self.db.users
        return users.insert_one(doc).inserted_id

    def add_item(self, item):
        doc = item.to_dict()
        if self.get_item(doc["user"], doc["name"]):
            raise ValueError("Item " + doc["name"] + " already exists for user " + doc["user"])
        doc['inUTC'] = datetime.datetime.utcnow()
        doc['version'] = 1
        items = self.db.items
        return items.insert_one(doc).inserted_id

    def get_user(self, username):
        users = self.db.users
        return users.find_one({"username": username})

    def get_users(self):
        return self.db.users.find({})

    def get_item(self, user, item):
        items = self.db.items
        return items.find_one({"id": user + item})

    def get_items(self, query):
        items = self.db.items
        return items.find(query)

    def set_item_claimed(self, username, itemname, claimed=True):
        item = self.get_item(username, itemname)
        item["claimed"] = claimed
        return self.update_item(item)

    def update_item(self, item):
        items = self.db.items
        current_item = self.get_item(item["user"], item["name"])
        if 'link' in item:
            current_item["link"] = item["link"]
        if 'claimed' in item:
            current_item["claimed"] = item["claimed"]
        current_item["version"] += 1
        current_item["inUTC"] = datetime.datetime.utcnow()
        return items.save(current_item)