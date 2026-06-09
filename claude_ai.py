import anthropic
import os

client = anthropic.Anthropic(api_key=os.environ.get('ANTHROPIC_API_KEY'))

SYSTEM_PROMPT = """คุณเป็นนักโหราศาสตร์จีนผู้เชี่ยวชาญ Bazi (四柱八字) วิเคราะห์ดวงชะตาจากข้อมูลที่ได้ โดย:
- อธิบายเป็นภาษาไทย กระชับ อ่านง่าย
- บอกธาตุหลัก (Day Master) และความหมาย
- วิเคราะห์ความสมดุลธาตุ
- บอกจุดแข็ง จุดอ่อน และแนวทางชีวิต
- ตอบไม่เกิน 300 คำ เหมาะกับ Line chat"""

def analyze_bazi(bazi_data: dict, birth_info: str) -> str:
    prompt = f"""วิเคราะห์ดวง Bazi นี้:
ข้อมูลเกิด: {birth_info}
เสาปี: {bazi_data['year']['combined']} ({bazi_data['year']['element']})
เสาเดือน: {bazi_data['month']['combined']} ({bazi_data['month']['element']})
เสาวัน (ตัวตน): {bazi_data['day']['combined']} ({bazi_data['day']['element']})
เสาชั่วโมง: {bazi_data['hour']['combined']} ({bazi_data['hour']['element']})
สัดส่วนธาตุ: {bazi_data['element_count']}"""

    response = client.messages.create(
                                              model="claude-opus-4-5",
                                              max_tokens=600,
                                              system=SYSTEM_PROMPT,
                                              messages=[{"role": "user", "content": prompt}]
    )
    return response.content[0].text
