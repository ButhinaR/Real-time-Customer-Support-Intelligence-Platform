from pydantic import BaseModel, ConfigDict

class Tweet(BaseModel):
    model_config = ConfigDict(strict=True)

    tweet_id: int
    author_id: str
    text: str
    created_at: str