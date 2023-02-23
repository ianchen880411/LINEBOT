from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *


#======這裡是呼叫的檔案內容=====
from message import *
from new import *
from Function import *
#======這裡是呼叫的檔案內容=====

#======python的函數庫==========
import tempfile, os
import datetime
import time
#======python的函數庫==========

app = Flask(__name__)
static_tmp_path = os.path.join(os.path.dirname(__file__), 'static', 'tmp')
# Channel Access Token
line_bot_api = LineBotApi('YK64/UiAEHdkl0LuQplUe+YNUVUJdK/beTjsk7DXssRVepTEIl231RPiUgyHFp9useLweRsptyU94eQNdBuYcznj2o98f5y11uF5J7r3wBcIaTqrcr4sfo4gzK7HW1n3JZ/zmgD20Y5JbhnMoq6SzQdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('0f3147643b839cf455e52661ab3a7918')


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


# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    msg = event.message.text
    if '我怕怕' in msg:
        msg_arr = []
        message = TextSendMessage(text='不怕不怕，包包保護妳')
        msg_arr.append(message)
        message = StickerSendMessage(
            package_id = '1070',
            sticker_id = '17866'
        )
        msg_arr.append(message)
        line_bot_api.reply_message(event.reply_token, msg_arr)
    elif '幫我找' in msg:
        if len(msg[3:]) == 0:
            message = TextSendMessage(text='好傢伙 請說妳想找什麼(ex:幫我找包包)') 
        else:
            message = TextSendMessage(text='https://www.google.com/search?q=' + msg[3:])
        line_bot_api.reply_message(event.reply_token, message)
    elif '包包愛我嗎' in msg:
        msg_arr = []
        message = StickerSendMessage(
            package_id = '11537',
            sticker_id = '52002736'
        )
        msg_arr.append(message)
        message = StickerSendMessage(
            package_id = '11537',
            sticker_id = '52002737'
        )
        msg_arr.append(message)
        line_bot_api.reply_message(event.reply_token, msg_arr)
    elif '是什麼' in msg:      
        message = TextSendMessage(text='https://www.google.com/search?q=' + msg[:-3])
        line_bot_api.reply_message(event.reply_token, message)
    elif '睡' in msg:
        msg_arr = []
        message = TextSendMessage(text='晚安，包包大軍、包包龜奴隸、還有包包保護妳')
        msg_arr.append(message)
        message = StickerSendMessage(
            package_id = '11537',
            sticker_id = '52002737'
        )
        msg_arr.append(message)
        line_bot_api.reply_message(event.reply_token, msg_arr)
    elif '功能列表' in msg:
        message = function_list()
        line_bot_api.reply_message(event.reply_token, message)
    else:
        message = TextSendMessage(text=msg)
        line_bot_api.reply_message(event.reply_token, message)

@handler.add(PostbackEvent)
def handle_message(event):
    print(event.postback.data)


@handler.add(MemberJoinedEvent)
def welcome(event):
    uid = event.joined.members[0].user_id
    gid = event.source.group_id
    profile = line_bot_api.get_group_member_profile(gid, uid)
    name = profile.display_name
    message = TextSendMessage(text=f'{name}歡迎加入，包包大軍準備好了')
    line_bot_api.reply_message(event.reply_token, message)
        
        
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
