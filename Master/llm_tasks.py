class LLMTask:
    def __init__(self, username: str, llm_name: str, tinyMMLU: int = 0, tinyHellaswag: int = 0, assigned: bool = False):
        self.username = username
        self.llm_name = llm_name
        self.tinyMMLU = tinyMMLU
        self.tinyHellaswag = tinyHellaswag
        self.assigned: bool = assigned
        self.accessed = False
    
    def __str__(self):
        return f"Task({self.username}, {self.llm_name}, tinyLLMU: {self.tinyMMLU}), tinyHellaswag: {self.tinyHellaswag}"

    def to_dict(self):
        return {
            "username": self.username,
            "llm_name": self.llm_name,
            "tinyMMLU": self.tinyMMLU,
            "tinyHellaswag": self.tinyHellaswag,
            "assigned": self.assigned
        }

    @staticmethod
    def from_dict(data: dict):
        return LLMTask(
            username=data["username"],
            llm_name=data["llm_name"],
            tinyMMLU=data.get("tinyMMLU", 0),
            tinyHellaswag=data.get("tinyHellaswag", 0),
            assigned=data.get("assigned", False)
        )
