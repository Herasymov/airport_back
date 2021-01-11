from api_admin.models import BaseModel
import pymongo


class MongoConnection(BaseModel):
    def __init__(self):
        self.myclient = pymongo.MongoClient("mongodb://localhost:27018/")
        self.mydb = self.myclient["mydatabase"]
        self.mycol = self.mydb["customers"]


class PostChatData(BaseModel):
    def __init__(self, data: dict):
        self.name = str(data["name"])
        self.review = str(data["review"])
        self.rating = str(data["rating"])


