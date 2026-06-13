from flask import Flask, request, abort
from dotenv import load_dotenv
import os
import requests

from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, LocationMessage

load_dotenv()

app = Flask(__name__)

CHANNEL_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")
CHANNEL_SECRET = os.getenv("LINE_CHANNEL_SECRET")
GOOGLE_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")
print("GOOGLE_API_KEY =", GOOGLE_API_KEY)

line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)


@app.route("/")
def home():
    return "Emergency Help Bot Running"


@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers["X-Line-Signature"]
    body = request.get_data(as_text=True)

    print("BODY =", body)
    print("SIGNATURE =", signature)

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
🚑 1668 กู้ชีพ
"""

    elif "ฮีตสโตรก" in user_text or "heatstroke" in user_text:
        reply_text = """☀️ ฮีตสโตรก

1. ย้ายผู้ป่วยเข้าที่ร่ม
2. คลายเสื้อผ้า
3. เช็ดตัวด้วยน้ำเย็น
4. ให้ดื่มน้ำหากยังรู้สึกตัวดี
5. โทร 1669

⚠️ อาจเป็นอันตรายถึงชีวิต
"""

    elif "ลมชัก" in user_text or "ชัก" in user_text:
        reply_text = """⚠️ ผู้ป่วยลมชัก

1. จัดพื้นที่รอบตัวให้ปลอดภัย
2. ตะแคงตัวผู้ป่วย
3. จับเวลาอาการชัก
4. โทร 1669 หากชักเกิน 5 นาที

❌ ห้ามง้างปาก
❌ ห้ามยัดสิ่งของเข้าปาก
"""

    elif "สุนัขกัด" in user_text or "หมากัด" in user_text:
        reply_text = """🐕 สุนัขกัด

1. ล้างแผลด้วยน้ำและสบู่ 15 นาที
2. กดห้ามเลือดหากมีเลือดออก
3. รีบพบแพทย์
4. ประเมินวัคซีนพิษสุนัขบ้า

⚠️ ห้ามปล่อยทิ้งไว้
"""

    elif "งูกัด" in user_text:
        reply_text = """🐍 งูกัด

1. อยู่นิ่งที่สุด
2. ลดการเคลื่อนไหวของอวัยวะที่ถูกกัด
3. โทร 1669
4. รีบไปโรงพยาบาล

❌ ห้ามกรีดแผล
❌ ห้ามดูดพิษ
❌ ห้ามขันชะเนาะแน่น
"""

    elif "ผึ้งต่อย" in user_text:
        reply_text = """🐝 ผึ้งต่อย

1. เอาเหล็กในออก
2. ล้างแผลด้วยน้ำสะอาด
3. ประคบเย็น
4. สังเกตอาการแพ้

⚠️ หากหายใจลำบาก โทร 1669
"""

    elif "แมงป่อง" in user_text:
        reply_text = """🦂 แมงป่องต่อย

1. ล้างแผล
2. ประคบเย็น
3. พักอวัยวะที่ถูกต่อย
4. พบแพทย์หากปวดมาก

⚠️ หากหายใจลำบาก โทร 1669
"""

    elif "ฉุกเฉิน" in user_text:
        reply_text = """🚨 เหตุฉุกเฉิน

☎️ 1669 แพทย์ฉุกเฉิน
🚓 191 ตำรวจ
🚒 199 ดับเพลิง

📍 หากสามารถส่งตำแหน่งได้ โปรดแจ้งตำแหน่งของคุณแก่เจ้าหน้าที่

⚠️ หากผู้ป่วยไม่หายใจ ให้เริ่ม CPR ทันที
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
☀️ ฮีตสโตรก
⚠️ ลมชัก
🐕 สุนัขกัด
🐍 งูกัด
🐝 ผึ้งต่อย
🦂 แมงป่องต่อย

🚨 ฉุกเฉิน
🏥 โรงพยาบาลใกล้ฉัน
📍 ส่งตำแหน่งของคุณ
☎️ เบอร์ฉุกเฉิน
"""

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply_text)
    )

@handler.add(MessageEvent, message=LocationMessage)
def handle_location(event):
    print("LOCATION RECEIVED")

    latitude = event.message.latitude
    longitude = event.message.longitude

    url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"

    params = {
        "location": f"{latitude},{longitude}",
        "radius": 50000,
        "type": "hospital",
        "key": GOOGLE_API_KEY
    }

    response = requests.get(url, params=params)
    data = response.json()

    print("GOOGLE RESPONSE =", data)

    hospitals = data.get("results", [])[:3]

    reply_text = "🏥 โรงพยาบาลใกล้คุณ\n\n"

    if hospitals:
        for i, hospital in enumerate(hospitals, start=1):
            name = hospital.get("name", "ไม่ทราบชื่อ")

            lat = hospital["geometry"]["location"]["lat"]
            lng = hospital["geometry"]["location"]["lng"]

            map_link = f"https://maps.google.com/?q={lat},{lng}"

            reply_text += f"{i}. {name}\n{map_link}\n\n"
    else:
        reply_text += "ไม่พบโรงพยาบาลใกล้เคียง\n"

    reply_text += "\n🚑 หากเป็นเหตุฉุกเฉิน โปรดโทร 1669"

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply_text)
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)