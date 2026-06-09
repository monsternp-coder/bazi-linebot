from flask import Flask, request, abort
from linebot.v3 import WebhookHandler
from linebot.v3.messaging import Configuration, ApiClient, MessagingApi, ReplyMessageRequest, TextMessage
from linebot.v3.webhooks import MessageEvent, TextMessageContent
from linebot.v3.exceptions import InvalidSignatureError
import re, os
from bazi_calc import calculate_bazi
from claude_ai import analyze_bazi

app = Flask(__name__)
configuration = Configuration(access_token=os.environ['LINE_CHANNEL_ACCESS_TOKEN'])
handler = WebhookHandler(os.environ['LINE_CHANNEL_SECRET'])
user_sessions = {}

@app.route("/webhook", methods=['POST'])
def webhook():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    user_id = event.source.user_id
    text = event.message.text.strip()
    reply = process_message(user_id, text)
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        line_bot_api.reply_message_with_http_info(
            ReplyMessageRequest(reply_token=event.reply_token, messages=[TextMessage(text=reply)])
        )

def process_message(user_id: str, text: str) -> str:
    if text in ["/start", "/bazi"]:
        return "ยินดีต้อนรับ Bazi Bot กรุณาพิมพ์วันเกิด เช่น 15/05/1990 14:00"
    date_pattern = r'(\d{1,2})[/\-](\d{1,2})[/\-](\d{4})\s*(\d{1,2}:\d{2})?'
    match = re.search(date_pattern, text)
    if match:
        try:
            day, month, year = int(match.group(1)), int(match.group(2)), int(match.group(3))
            if year > 2400: year -= 543
            time_str = match.group(4)
            hour = int(time_str.split(':')[0]) if time_str else 12
            bazi = calculate_bazi(year, month, day, hour)
            birth_info = f"{day}/{month}/{year} เวลา {hour}:00 น."
            card = (f"ดวง Bazi ของคุณ\n{'─'*20}\n"
                   f"เสาปี: {bazi['year']['combined']}\n"
                   f"เสาเดือน: {bazi['month']['combined']}\n"
                   f"เสาวัน: {bazi['day']['combined']} (ตัวตน)\n"
                   f"เสาชม: {bazi['hour']['combined']}\n{'─'*20}")
            analysis = analyze_bazi(bazi, birth_info)
            return f"{card}\n\nการวิเคราะห์:\n{analysis}"
        except:
            return "รูปแบบไม่ถูกต้อง กรุณาพิมพ์ เช่น 15/05/1990 14:00"
    return "พิมพ์วันเกิดเพื่อคำนวณดวง เช่น 15/05/1990 14:00 หรือ /bazi"

if __name__ == "__main__":
    app.run(port=8080)
