from pydantic import Field, BaseSettings


class MongoSettings(BaseSettings):
    mongodb_uri: str = Field(...,env='MONGO_URL')
