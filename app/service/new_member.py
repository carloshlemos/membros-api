from app.repository.new_member import NewMemberRepository


class NewMemberService:
    def __init__(self):
        self.repository = NewMemberRepository()

    def get_by_celular(self, celular: str):
        return self.repository.get_by_celular(celular)

    def update_new_member(self, celular: str, data):
        update_data = data.dict(exclude_unset=True)
        update_data["celular"] = celular
        self.repository.update(celular, update_data)
        return self.get_by_celular(celular)
