from app.repository.new_member import NewMemberRepository
from app.security import create_access_token


class NewMemberService:
    def __init__(self):
        self.repository = NewMemberRepository()

    def generate_token(self, telefone: str):
        token = create_access_token(data={"sub": telefone})
        self.repository.save(token, telefone)
        return token
