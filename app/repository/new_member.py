from ..mongo import get_mongodb


class NewMemberRepository:
    def __init__(self):
        self.db = get_mongodb()
        self.collection = self.db.get_collection("new_members")

    def save(self, token: str, celular: str):
        self.collection.update_one(
            {"celular": celular},
            {"$set": {"token": token, "celular": celular}},
            upsert=True
        )

    def update(self, celular: str, data: dict):
        self.collection.update_one(
            {"celular": celular},
            {"$set": data},
            upsert=True
        )

    def get_by_celular(self, celular: str):
        return self.collection.find_one({"celular": celular})


