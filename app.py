from flask import Flask, request, abort
from dotenv import load_dotenv
import os

from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

load_dotenv()

app = Flask(__name__)

CHANNEL_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")
CHANNEL_SECRET = os.getenv("LINE_CHANNEL_SECRET")

line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)


@app.route("/")
def home():
    return "Emergency Help Bot Running"


@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers["X-Line-Signature"]
    body = request.get_data(as_text=True)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return "OK"


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_text = event.message.text.strip()

    print("ได้รับข้อความ:", user_text)

    if "ไฟไหม้" in user_text:
        reply_text = """🔥 เหตุไฟไหม้

1. อพยพออกจากพื้นที่ทันที
2. โทร 199 แจ้งดับเพลิง
3. หากมีควัน ให้ก้มต่ำและใช้ผ้าปิดจมูก
4. ห้ามใช้ลิฟต์

❌ ห้ามกลับเข้าอาคาร
"""

    elif "หมดสติ" in user_text:
        reply_text = """🚑 ผู้ป่วยหมดสติ

1. ตรวจการตอบสนอง
2. ตรวจการหายใจ
3. โทร 1669
4. หากไม่หายใจ ให้เริ่ม CPR
"""

    elif "เลือดออก" in user_text:
        reply_text = """🩸 เลือดออก

1. ใช้ผ้าสะอาดกดแผล
2. ยกบริเวณแผลให้สูง
3. กดแผลต่อเนื่อง
4. โทร 1669 หากเลือดไม่หยุด
"""

    elif "ไฟฟ้าช็อต" in user_text:
        reply_text = """⚡ ไฟฟ้าช็อต

1. ตัดกระแสไฟก่อน
2. อย่าสัมผัสผู้บาดเจ็บโดยตรง
3. โทร 1669
4. ตรวจการหายใจ
"""

    elif "หัวใจหยุดเต้น" in user_text or "CPR" in user_text:
        reply_text = """❤️ หัวใจหยุดเต้น

1. โทร 1669
2. เริ่ม CPR
3. กดหน้าอก 100-120 ครั้ง/นาที
4. ใช้ AED หากมี
"""

    elif "น้ำร้อนลวก" in user_text:
        reply_text = """♨️ การปฐมพยาบาลน้ำร้อนลวก

1. เปิดน้ำสะอาดผ่านแผล 10-20 นาที
2. ถอดเครื่องประดับใกล้แผล
3. ปิดแผลด้วยผ้าสะอาด

❌ ห้ามทายาสีฟัน
❌ ห้ามเจาะตุ่มพอง
❌ ห้ามทาน้ำปลา
"""

    elif "แผลถลอก" in user_text:
        reply_text = """🩹 การปฐมพยาบาลแผลถลอก

1. ล้างแผลด้วยน้ำสะอาด
2. เช็ดรอบแผลให้แห้ง
3. ทายาฆ่าเชื้อ
4. ปิดแผลหากจำเป็น
"""

    elif "เลือดกำเดาไหล" in user_text:
        reply_text = """👃 วิธีปฐมพยาบาลเลือดกำเดาไหล

1. นั่งตัวตรง
2. ก้มหน้าเล็กน้อย
3. บีบจมูก 10-15 นาที
4. หายใจทางปาก
"""

    elif "เป็นลม" in user_text:
        reply_text = """😵 วิธีช่วยผู้เป็นลม

1. พาไปในที่อากาศถ่ายเท
2. ให้นอนราบ
3. ยกขาสูงเล็กน้อย
4. คลายเสื้อผ้าที่รัดแน่น

☎️ หากไม่ฟื้น โทร 1669
"""

    elif "สำลักอาหาร" in user_text:
        reply_text = """🍽️ การช่วยผู้สำลักอาหาร

1. กระตุ้นให้ไอ
2. หากหายใจไม่ได้ โทร 1669
3. ใช้ Heimlich Maneuver
"""

    elif "แมลงกัดต่อย" in user_text:
        reply_text = """🦟 การปฐมพยาบาลแมลงกัดต่อย

1. ล้างบริเวณที่ถูกกัด
2. ประคบเย็น
3. ทายาลดอาการคัน

☎️ หากหายใจลำบาก โทร 1669
"""

    elif "เบอร์ฉุกเฉิน" in user_text:
        reply_text = """☎️ เบอร์ฉุกเฉิน

🚑 1669 แพทย์ฉุกเฉิน
🚒 199 ดับเพลิง
🚓 191 ตำรวจ
🚨 1784 ปภ.
"""

    else:
        reply_text = """🚑 Emergency Help Bot

🔥 ไฟไหม้
🚑 หมดสติ
🩸 เลือดออก
⚡ ไฟฟ้าช็อต
❤️ หัวใจหยุดเต้น

♨️ น้ำร้อนลวก
🩹 แผลถลอก
👃 เลือดกำเดาไหล
😵 เป็นลม
🍽️ สำลักอาหาร
🦟 แมลงกัดต่อย

☎️ เบอร์ฉุกเฉิน
"""

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply_text)
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
