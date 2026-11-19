# -*- coding: utf-8 -*-
# สร้างชุดสอบซ่อมระดับกลาง (2026-11-19) สำหรับนักเรียนที่สอบชุด Advance ไม่ผ่าน
#   source/advance-makeup.json  40 ข้อ บทละ 8 ข้อ ข้อใหม่ 4 ข้อ ข้อเดิมจากชุด Advance 4 ข้อ
#   เรียงข้อตามลำดับในไฟล์ (สลับคละบทไว้แล้ว) คำตอบถูกอยู่ตัวเลือกแรกเหมือนไฟล์ source อื่น
#   ข้อเดิมมีช่อง "orig" = ลำดับข้อในชุด Advance (0–39) สคริปต์ย้ายคำตอบไม่ให้ตรงตำแหน่งเดิม
#   และกระจายคำตอบ ก ข ค ง ให้เท่ากันตำแหน่งละ 10 ข้อ
# แก้ข้อสอบให้แก้ใน source แล้วรัน python3 data/build-makeup-2026-11.py ได้ quiz-makeup-2026-11.json
# เอาขึ้นใช้งานด้วย add-makeup.html
import json, io, os

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "source")

rows = json.load(io.open(os.path.join(SRC, "advance-makeup.json"), encoding="utf-8"))
assert len(rows) == 40, len(rows)

# ตำแหน่งคำตอบของข้อเดิมในชุด Advance (build-quiz-2026-10.py ใช้ ลำดับ % 4)
avoid = [r["orig"] % 4 if r.get("orig") is not None else None for r in rows]

# จับคู่ตำแหน่งคำตอบ ตำแหน่งละ 10 ข้อ ข้อเดิมห้ามตรงตำแหน่งเดิม (ค้นแบบย้อนกลับ ข้อน้อย จบเร็ว)
pos = [None] * 40
left = [10, 10, 10, 10]


def solve(i):
    if i == 40:
        return True
    # เริ่มจาก i % 4 ให้ไล่ตำแหน่งหมุนวนเหมือนชุดอื่น
    for k in range(4):
        p = (i + k) % 4
        if left[p] and p != avoid[i]:
            pos[i] = p; left[p] -= 1
            if solve(i + 1):
                return True
            left[p] += 1
    return False


assert solve(0)

qs = []
for r, p in zip(rows, pos):
    ch = r["ch"]
    assert len(ch) == 4 and len(set(ch)) == 4, r["q"]
    qs.append({"cat": r["cat"], "q": r["q"], "ch": ch[1:p + 1] + [ch[0]] + ch[p + 1:],
               "ans": p, "ex": r["ex"], "img": ""})

data = {"adv1r": {
    "name": "Advance สอบซ่อม", "label": "ADVANCE · สอบซ่อม", "level": "ระดับกลาง",
    "order": 2.5, "active": True,
    "desc": "ชุดสอบซ่อมของระดับกลาง ใช้เมื่อสอบชุด Advance ไม่ผ่าน · ห้าบทเดียวกัน คละข้อใหม่กับข้อเดิม",
    "qs": qs,
}}
io.open(os.path.join(HERE, "quiz-makeup-2026-11.json"), "w", encoding="utf-8").write(
    json.dumps(data, ensure_ascii=False, indent=1))
reused = sum(1 for a in avoid if a is not None)
print("เขียน quiz-makeup-2026-11.json", len(qs), "ข้อ · ข้อเดิม", reused, "· ข้อใหม่", 40 - reused,
      "· ตำแหน่งคำตอบ", [pos.count(i) for i in range(4)])
