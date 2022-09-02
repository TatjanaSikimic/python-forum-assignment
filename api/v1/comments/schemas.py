from api.base.schemas import BaseModel


class BaseComment(BaseModel):
    pass  # Needs to have text


class CommentUpdate(BaseComment):
    pass


