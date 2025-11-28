from ..mongo import get_mongodb


class NewMemberRepository:
    def __init__(self):
        self.db = get_mongodb()
        self.collection = self.db.get_collection("new_members")

    def save(self, token: str, telefone: str):
        self.collection.update_one(
            {"telefone": telefone},
            {"$set": {"token": token, "telefone": telefone}},
            upsert=True
        )

    def update(self, telefone: str, data: dict):
        self.collection.update_one(
            {"telefone": telefone},
            {"$set": data},
            upsert=True
        )

    def get_by_telefone(self, telefone: str):
        return self.collection.find_one({"telefone": telefone})


