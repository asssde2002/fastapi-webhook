from fastapi import FastAPI, HTTPException, Request, Depends
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import TextMessage, MessageEvent, TextSendMessage, StickerMessage
from database import engine, get_db
import uvicorn, os, models, schemas
from sqlalchemy.orm import Session
from utils import check_line_token
import datetime


app = FastAPI()
models.Base.metadata.create_all(bind=engine)


LINE_CHANNEL_ACCESS_TOKEN = os.environ.get('LINE_CHANNEL_ACCESS_TOKEN')
LINE_CHANNEL_SECRET = os.environ.get('LINE_CHANNEL_SECRET')
LINE_CHANNEL_ID = os.environ.get('LINE_CHANNEL_ID')
API_KEY = os.environ.get('API_KEY')


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/line-webhook/")
async def line_webhook(request: Request, db: Session = Depends(get_db)):
    line_channel_id = request.query_params.get('line_channel_id')
    if not line_channel_id:
        raise HTTPException(status_code=400, detail="LineChannelID is missing")
    
    line_channel = models.LineChannel.get_line_channel(db, line_channel_id)
    if not line_channel:
        raise HTTPException(status_code=400, detail=f"No corresponding line channel: {line_channel_id}")
    else:
        line_channel = check_line_token(db, line_channel)
    
    body = await request.json()
    event = body.get('events')
    if len(event) > 0 and type(event) == list:
        event = event[0]
        line_id = event['source']['userId']
        replyToken = event['replyToken']
        messages = f"Your line_id is: {line_id}"
        messages = TextSendMessage(messages)
        line_bot_api = LineBotApi(line_channel.line_channel_access_token)
        line_bot_api.reply_message(replyToken, messages=messages)
    
    return 'OK'


@app.post("/line-channel/")
async def create_line_channel(request: Request, db: Session = Depends(get_db)):
    body = await request.json()
    api_key = body.get('api_key')
    line_channel_id = body.get('line_channel_id')
    line_channel_name = body.get('line_channel_name')
    line_channel_secret = body.get('line_channel_secret')
    line_channel_access_token = body.get('line_channel_access_token')
    if api_key != API_KEY:
        raise HTTPException(status_code=404, detail="APIKEY is wrong")
    
    if not line_channel_id:
        raise HTTPException(status_code=400, detail="LineChannelID is missing")

    line_channel = models.LineChannel.get_line_channel(db, line_channel_id)
    if not line_channel:
        line_channel = models.LineChannel(line_channel_id=line_channel_id)
            
    if line_channel_name:
        setattr(line_channel, 'line_channel_name', line_channel_name)
        
    if line_channel_secret:
        setattr(line_channel, 'line_channel_secret', line_channel_secret)
    
    if line_channel_access_token:
        setattr(line_channel, 'line_channel_access_token', line_channel_access_token)
    
    setattr(line_channel, 'updated_at', datetime.datetime.utcnow())
    db.add(line_channel)
    db.commit()
    db.refresh(line_channel)
    return line_channel


if __name__ == '__main__':
    uvicorn.run("main:app", host="localhost", port=5000, reload=True)
