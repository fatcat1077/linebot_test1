
#載入LineBot所需要的套件
from flask import Flask, request, abort
import json
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *
import re

app = Flask(__name__)

# 放上自己的Channel Access Token
line_bot_api = LineBotApi('pGgY+7o+KHhCxmQvMt8EFk6JDp+ynVH4x30OlPH+htI2wj3ACCL+rZLw28ulzjnzF+d8r20m1KeYjvqPC+b3r1i1SvWXfrsX4GZC9k6F3s78tZXpqL/rAvZrMwMGCegWh1EL9/SzEM9jgSHUYQFd8QdB04t89/1O/w1cDnyilFU=')
# 放上自己的Channel Secret
handler = WebhookHandler('a858b6490ab19aece43c10f4b775bdf2')

# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

#訊息傳遞區塊
##### 基本上程式編輯都在這個function #####
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
        word=event.message.text
        word=word.lower().strip()
        if re.match('我需要一點迷因',word):
            imagemap_message = ImagemapSendMessage(
                base_url='https://i.imgur.com/ZoLFq9S.png',#組圖
                alt_text='this is an imagemap',#預設
                base_size=BaseSize(height=1040, width=1040),
                video=Video(
                    original_content_url='https://i.imgur.com/1Y5IgRm.mp4',#John Cena!!!
                    preview_image_url='https://i.imgur.com/UShDjCV.jpg',#John photo
                    area=ImagemapArea(
                        x=0, y=0, width=1040, height=585
                    ),
                    external_link=ExternalLink(# 影片結束後的連結
                        link_uri='https://www.youtube.com/watch?v=_L9kvyVMR0M',
                        label='More about John Cena',
                    ),
                ),
                actions=[
                    URIImagemapAction(# 超連結
                        link_uri='https://www.youtube.com/watch?v=dQw4w9WgXcQ',
                        area=ImagemapArea(
                            x=0, y=585, width=520, height=455
                        )
                    ),
                    URIImagemapAction(# 超連結
                        link_uri='https://www.youtube.com/watch?v=C5zTO4nhXl4',
                        area=ImagemapArea(
                            x=520, y=585, width=520, height=455
                        )
                    )
                ]
            )
            line_bot_api.reply_message(event.reply_token, imagemap_message)
        else:
            try:  
                with open('diction6700.json',mode='r+',encoding='UTF-8') as file:
                    data=json.load(file)
                    defi=data[word][0]
                    message = TextSendMessage(text=(event.message.text+'的定義是：\n'+defi))
                    line_bot_api.reply_message(event.reply_token,message)
            except Exception:
                message = TextSendMessage(text=(event.message.text+'的搜尋有誤，請嘗試：\n1.輸入7000單有的單字\n2.稍等一下再嘗試\n3.我需要一點迷因'))
                line_bot_api.reply_message(event.reply_token,message)


#主程式
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)