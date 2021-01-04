from api_admin.models import BaseModel


class PostChatData(BaseModel):
    def __init__(self, data: dict):
        self.name = str(data["name"])
        self.review = str(data["review"])
        self.rating = str(data["rating"])

