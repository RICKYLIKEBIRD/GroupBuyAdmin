import db
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import FlexSendMessage, TextSendMessage, MessageEvent, TextMessage, PostbackEvent,FollowEvent

from model.admin_user import adminUser
import logging

#主程式
import os

dataBase = db.initDb()

app = Flask(__name__)

# 部署上render.com時要註解
from dotenv import load_dotenv
load_dotenv('dev.env')

# Channel Access Token
line_bot_api = LineBotApi(os.getenv('CHANNEL_ACCESS_TOKEN'))
# Channel Secret
handler = WebhookHandler(os.getenv('CHANNEL_SECRET'))

# @app.route("/alive",methods=['GET','POST'])
# def alive():
#     return "alive"

@app.route("/api", methods=['POST','GET'])
def api():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

 
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    if request.method == 'GET':
        app.logging.info('get this')
    else :
    # handle webhook body
        try:
            handler.handle(body, signature)
        except InvalidSignatureError:
            abort(400)

        return 'OK'
    


@handler.add(FollowEvent)
def handle_follow(event):
    sourse = event.source
    app.logger.info(sourse)
    user_id = sourse.user_id

    admin_user = adminUser()
    admin_user.user_id = user_id
    admin_user.user_name = 'user_name'

    db.insertAdminUser(dataBase, admin_user)

#訊息傳遞區塊
##### 基本上程式編輯都在這個function #####
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    message = TextSendMessage(text=event.message.text)

    # if message.text == 'menu':
    #     flex_message = FlexSendMessage(alt_text="hello", contents="generate_main_menu()")
    #     line_bot_api.reply_message(
    #         event.reply_token,
    #         flex_message
    #     )
    # else :
    line_bot_api.reply_message(event.reply_token,message)

    app.logger.info("show event: ")
    app.logger.info(event)
    
@handler.add(PostbackEvent)
def handle_postback(event):
    
    postback_data = event.postback.data
    postback_params = event.postback.params
    app.logger.info("show postback_params start")
    app.logger.info(postback_params)
    app.logger.info("show postback_params end")

    if postback_data == 'dateTimePick':

        reply_message = FlexSendMessage(alt_text="time",contents="generate_date_pick()")
        line_bot_api.reply_message(event.reply_token, reply_message)

    elif postback_data == 'pickTime':

        message_content = f"這是你選擇的時間:  {postback_params['date']}"
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=message_content))

    # line_bot_api.reply_message(event.reply_token, reply_message)


# gunicorn_logger = logging.getLogger('gunicorn.error')
# app.logger.handlers = gunicorn_logger.handlers
# app.logger.setLevel(gunicorn_logger.level)


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
    