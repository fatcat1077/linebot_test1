# -*- coding: utf-8 -*-
"""
Created on Wed Jun  2 21:16:35 2021

@author: Ivan
版權屬於「行銷搬進大程式」所有，若有疑問，可聯絡ivanyang0606@gmail.com

Line Bot聊天機器人
第一章 Line Bot申請與串接
Line Bot機器人串接與測試
"""
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

app = Flask(__name__)

# 必須放上自己的Channel Access Token
line_bot_api = LineBotApi('pGgY+7o+KHhCxmQvMt8EFk6JDp+ynVH4x30OlPH+htI2wj3ACCL+rZLw28ulzjnzF+d8r20m1KeYjvqPC+b3r1i1SvWXfrsX4GZC9k6F3s78tZXpqL/rAvZrMwMGCegWh1EL9/SzEM9jgSHUYQFd8QdB04t89/1O/w1cDnyilFU=')
# 必須放上自己的Channel Secret
handler = WebhookHandler('a858b6490ab19aece43c10f4b775bdf2')

line_bot_api.push_message('Ue8e85ddfa7ca3ba12ace6b481ce59d3a', TextSendMessage(text='請輸入一個單字eg：cattle'))

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
#message = TextSendMessage(text=event.message.text)
#line_bot_api.reply_message(event.reply_token,message)
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    try:  
        with open('diction6700.json',mode='r+',encoding='UTF-8') as file:
            data=json.load(file)
            word=event.message.text
            word=word.lower()
            defi=data[word][0]
            message = TextSendMessage(text=(event.message.text+'的定義是：\n'+defi))
            line_bot_api.reply_message(event.reply_token,message)
    except Exception:
        message = TextSendMessage(text=(event.message.text+'的搜尋有誤，請嘗試：\n1.輸入7000單有的單字\n2.稍等一下再嘗試'))
        line_bot_api.reply_message(event.reply_token,message)


#主程式
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)