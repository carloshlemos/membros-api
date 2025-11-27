from zoneinfo import ZoneInfo

from ..domain import schemas
from ..mongo import get_mongodb

TZ = ZoneInfo("America/Sao_Paulo")


class MembroRepository:
    def __init__(self):
        self.db = get_mongodb()
        self.collection = self.db['membros']

    def find_by_id(self, membro_id: str):
        return self.collection.find_one({"id": membro_id})

    def update(self, membro_id: str, data: dict):
        self.collection.update_one({"id": membro_id}, {"$set": data})
        return self.find_by_id(membro_id)

    def find_all(self, filters: dict, skip: int, limit: int, sort_by: str = "nome", sort_order: int = 1):
        query = {}
        for key, value in filters.items():
            if isinstance(value, str):
                query[key] = {"$regex": value, "$options": "i"}
            else:
                query[key] = value

        cursor = (
            self.collection
            .find(query)
            .sort(sort_by, sort_order)
            .skip(skip)
            .limit(limit)
        )

        total = self.collection.count_documents(query)
        membros = list(cursor)

        return total, [schemas.Membro(**doc) for doc in membros]