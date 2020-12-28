class BaseModel:
    def __repr__(self):
        return f"dict for class {self.__class__.__name__} \n\t" + "\n\t".join(
            [f"{key}: {value}" for key, value in self.__dict__.items()])
