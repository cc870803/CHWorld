from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

line_bot_api = LineBotApi('+IaZTysiQhwRVKezaCqupuW+Y5VxgyAjmKQElJ2JKuKG7RoRPTLRrE8J8q0Mx27oKQyG0jyq4zV/ZLXaR7VdnuEn3rLlvHzHCaQ5iNnHDOIjD2uzqzCJywaS6Pu5sdAd+s+oLMKlbsCIzrhtuXR3uAdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('a38fc53dd3fc9f9952774d6dae9a3754')


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
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run()