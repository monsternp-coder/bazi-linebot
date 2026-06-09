import sxtwl

Gan = ["甲","乙","丙","丁","戊","己","庚","辛","壬","癸"]
Zhi = ["子","丑","寅","卯","辰","巳","午","未","申","酉","戌","亥"]
GanThai = ["เจี่ย","อี่","ปิ่ง","ติง","อู้","จี่","เกิง","ซิน","เหริน","กุ้ย"]
ZhiThai = ["จื่อ","โฉ่ว","อิน","เหมา","เฉิน","ซื่อ","อู่","เว่ย","เซิน","โหยว","ซู","ไห่"]
Element = {"甲":"ไม้+","乙":"ไม้-","丙":"ไฟ+","丁":"ไฟ-","戊":"ดิน+",
           "己":"ดิน-","庚":"ทอง+","辛":"ทอง-","壬":"น้ำ+","癸":"น้ำ-"}

def calculate_bazi(year: int, month: int, day: int, hour: int) -> dict:
    d = sxtwl.fromSolar(year, month, day)

    pillars = {
        "year":  (d.getYearGZ(True),  "ปี (祖先/วัยเด็ก)"),
        "month": (d.getMonthGZ(),      "เดือน (พ่อแม่/การงาน)"),
        "day":   (d.getDayGZ(),        "วัน (ตัวตน/คู่ครอง)"),
        "hour":  (d.getHourGZ(hour),   "ชั่วโมง (ลูก/อนาคต)"),
    }

    result = {}
    element_count = {}

    for key, (gz, meaning) in pillars.items():
        stem = Gan[gz.tg]
        branch = Zhi[gz.dz]
        elem = Element[stem]
        element_count[elem[:2]] = element_count.get(elem[:2], 0) + 1
        result[key] = {
            "stem": stem,
            "branch": branch,
            "combined": stem + branch,
            "element": elem,
            "meaning": meaning
        }

    result["element_count"] = element_count
    result["day_master"] = result["day"]["stem"]
    return result
