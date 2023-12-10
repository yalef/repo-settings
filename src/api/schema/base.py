import pydantic


class Repository(pydantic.BaseModel):
    name: str
    full_name: str
    id: int
    node_id: str
    private: bool


class Installation(pydantic.BaseModel):
    id: int
