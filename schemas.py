from pydantic import BaseModel


class LineChannel(BaseModel):
    line_channel_id: str
    line_channel_name: str
    line_channel_secret: str
    line_channel_access_token: str
    
    class Config:
        orm_mode = True
    