from ..mongo import get_mongodb


class NewMemberRepository:
    def __init__(self):
        self.db = get_mongodb()
        self.collection = self.db.get_collection("new_members")

    def save(self, token: str, telefone: str):
        self.collection.insert_one({"token": token, "telefone": telefone})
