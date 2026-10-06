# -*- coding: utf-8 -*-
# สร้างข้อสอบสามระดับ ระดับละ 40 ข้อ (2026-10-06) ออกจากคู่มือคอร์สของ Fixlikepro ฉบับปัจจุบัน
#   Basic    ระดับต้น   source/basic.json            คู่มือระดับเบื้องต้น 5 บท
#   Advance  ระดับกลาง  source/advance-ch1..5.json   คู่มือระดับกลาง บทละ 8 ข้อ
#   Pro      ระดับสูง   source/pro-ch1..5.json       คู่มือระดับสูง บทละ 8 ข้อ
# ไฟล์ใน source เขียนคำตอบถูกไว้ตัวเลือกแรก สคริปต์วนตำแหน่งคำตอบ 0 1 2 3 ให้กระจายเท่ากัน
# แก้ข้อสอบให้แก้ใน source แล้วรัน python3 data/build-quiz-2026-10.py ได้ไฟล์ quiz-2026-10.json
import json, io, os

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "source")


def load(names):
    rows = []
    for n in names:
        rows += json.load(io.open(os.path.join(SRC, n), encoding="utf-8"))
    return rows


def build(rows):
    out = []
    for i, r in enumerate(rows):
        ch = r["ch"]
        assert len(ch) == 4 and len(set(ch)) == 4, r["q"]
        pos = i % 4
        out.append({"cat": r["cat"], "q": r["q"], "ch": ch[1:pos + 1] + [ch[0]] + ch[pos + 1:],
                    "ans": pos, "ex": r["ex"], "img": ""})
    assert len(out) == 40, len(out)
    return out


SETS = {
    "basic1": {"name": "Basic", "label": "BASIC", "level": "ระดับต้น", "order": 1, "active": True,
               "desc": "โครงสร้างเครื่อง · ความปลอดภัย · เครื่องมือพื้นฐาน · แกะ ประกอบ เปลี่ยนอะไหล่ · ราคาและร้าน",
               "src": ["basic.json"]},
    "adv1":   {"name": "Advance", "label": "ADVANCE", "level": "ระดับกลาง", "order": 2, "active": True,
               "desc": "วงจรและผังวงจร · เครื่องมือวัด · เปลี่ยนไอซีและบอร์ดสองชั้น · กระแสและเปิดไม่ติด · ชาร์จและจอ",
               "src": ["advance-ch%d.json" % i for i in range(1, 6)]},
    "adv2":   {"name": "Pro", "label": "PRO", "level": "ระดับสูง", "order": 3, "active": True,
               "desc": "หน่วยประมวลผล · กู้ข้อมูลย้ายบอร์ด · ภาคสัญญาณ · เครื่องมือระดับสูง · วิเคราะห์การกินกระแสไฟ",
               "src": ["pro-ch%d.json" % i for i in range(1, 6)]},
}

data = {}
for key, s in SETS.items():
    meta = {k: v for k, v in s.items() if k != "src"}
    meta["qs"] = build(load(s["src"]))
    data[key] = meta
# ชุด Basic H2 เดิมรวมเข้า Basic แล้ว ซ่อนไว้ ไม่ลบ ผลสอบเก่ายังอยู่
data["basic2"] = {"active": False}

io.open(os.path.join(HERE, "quiz-2026-10.json"), "w", encoding="utf-8").write(
    json.dumps(data, ensure_ascii=False, indent=1))
print("เขียน quiz-2026-10.json", {k: len(v.get("qs", [])) for k, v in data.items()})
