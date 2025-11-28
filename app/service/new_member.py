from app.repository.new_member import NewMemberRepository
from app.security import create_access_token


class NewMemberService:
    def __init__(self):
        self.repository = NewMemberRepository()

    def generate_token(self, telefone: str):
        token = create_access_token(data={"sub": telefone})
        self.repository.save(token, telefone)
        return token

    def update_new_member(self, telefone: str, data):
        update_data = data.dict(exclude_unset=True)
        update_data["telefone"] = telefone
        self.repository.update(telefone, update_data)

    def get_by_telefone(self, telefone: str):
        return self.repository.get_by_telefone(telefone)


