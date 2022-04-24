import datetime
from sqlalchemy import Column, Integer, String, DateTime
from database import Base


class LineChannel(Base):
    __tablename__ = 'line_channels'
    id = Column(Integer, primary_key=True, index=True)
    line_channel_id = Column(String, index=True, unique=True)
    line_channel_name = Column(String, index=True)
    line_channel_secret = Column(String, index=True)
    line_channel_access_token = Column(String, index=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    @staticmethod
    def get_line_channel(db, line_channel_id):
        line_channel = db.query(LineChannel).filter(LineChannel.line_channel_id == line_channel_id).first()
        return line_channel
        
    