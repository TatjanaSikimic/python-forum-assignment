from api.base.schemas import BaseModel


class BaseComment(BaseModel):
    title: str  # Needs to have text
    content: str


class CommentUpdate(BaseComment):
    pass


