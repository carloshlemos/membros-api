from app.repository.new_member import NewMemberRepository
from app.security import create_access_token


class NewMemberService:
    def __init__(self):
        self.repository = NewMemberRepository()

    def generate_token(self, celular: str):
        token = create_access_token(data={"sub": celular})
        self.repository.save(token, celular)
        return token

    def update_new_member(self, celular: str, data):
        update_data = data.dict(exclude_unset=True)
        update_data["celular"] = celular
        self.repository.update(celular, update_data)

    def get_by_celular(self, celular: str):
        return self.repository.get_by_celular(celular)


