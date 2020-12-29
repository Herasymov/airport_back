class BaseModel:
    def __repr__(self):
        return f"dict for class {self.__class__.__name__} \n\t" + "\n\t".join(
            [f"{key}: {value}" for key, value in self.__dict__.items()])

class HasPagination(BaseModel):
    def __init__(self, data):
        self.page = int(data["page"]) -1
        self.limit = int(data["limit"])
        if self.page < 0 or self.limit <= 0:
            raise ValueError

        self.offset = self.page * self.limit


class HasValuePagination(BaseModel):
    def __init__(self, data):
        self.limit = int(data["limit"])
        if self.limit <= 0:
            raise ValueError

        try:
            self.last_id = int(data["lastId"])
        except:
            self.last_id = None
