# -*- coding: utf-8 -*-
# สร้างชุดสอบซ่อม (2026-11-19) สำหรับนักเรียนที่สอบชุดแรกไม่ผ่าน สองชุด
#   adv1r   ระดับกลาง  source/advance-makeup.json  ชุดแรก = adv1 (Advance)
#   basic1r ระดับต้น   source/basic-makeup.json    ชุดแรก = basic1 (Basic)
#   ชุดละ 40 ข้อ คละข้อใหม่กับข้อเดิม เรียงข้อตามลำดับในไฟล์ คำตอบถูกอยู่ตัวเลือกแรกเหมือนไฟล์ source อื่น
#   ข้อเดิมมีช่อง "orig" = ลำดับข้อในชุดแรก (0–39) สคริปต์ย้ายคำตอบไม่ให้ตรงตำแหน่งเดิม
#   และกระจายคำตอบ ก ข ค ง ให้เท่ากันตำแหน่งละ 10 ข้อ
# แก้ข้อสอบให้แก้ใน source แล้วรัน python3 data/build-makeup-2026-11.py ได้ quiz-makeup-2026-11.json
# เอาขึ้นใช้งานด้วย update-2026-11.html ขั้นที่ 1
import json, io, os

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "source")


def build(fname):
    rows = json.load(io.open(os.path.join(SRC, fname), encoding="utf-8"))
    assert len(rows) == 40, (fname, len(rows))
    # ตำแหน่งคำตอบของข้อเดิมในชุดแรก (build-quiz-2026-10.py ใช้ ลำดับ % 4)
    avoid = [r["orig"] % 4 if r.get("orig") is not None else None for r in rows]
    pos = [None] * 40
    left = [10, 10, 10, 10]

    # จับคู่ตำแหน่งคำตอบ ตำแหน่งละ 10 ข้อ ข้อเดิมห้ามตรงตำแหน่งเดิม (ค้นแบบย้อนกลับ เริ่มจาก i % 4)
    def solve(i):
        if i == 40:
            return True
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
    reused = sum(1 for a in avoid if a is not None)
    print(fname, len(qs), "ข้อ · ข้อเดิม", reused, "· ข้อใหม่", 40 - reused,
          "· ตำแหน่งคำตอบ", [pos.count(i) for i in range(4)])
    return qs


data = {
    "basic1r": {
        "name": "Basic สอบซ่อม", "label": "BASIC · สอบซ่อม", "level": "ระดับต้น",
        "order": 1.5, "active": True,  # พี่ทิเบตตรวจผ่าน 2026-11-20
        "desc": "ชุดสอบซ่อมของระดับต้น ใช้เมื่อสอบชุด Basic ไม่ผ่าน · ห้าบทเดียวกัน คละข้อใหม่กับข้อเดิม",
        "qs": build("basic-makeup.json"),
    },
    "adv1r": {
        "name": "Advance สอบซ่อม", "label": "ADVANCE · สอบซ่อม", "level": "ระดับกลาง",
        "order": 2.5, "active": True,
        "desc": "ชุดสอบซ่อมของระดับกลาง ใช้เมื่อสอบชุด Advance ไม่ผ่าน · ห้าบทเดียวกัน คละข้อใหม่กับข้อเดิม",
        "qs": build("advance-makeup.json"),
    },
}
io.open(os.path.join(HERE, "quiz-makeup-2026-11.json"), "w", encoding="utf-8").write(
    json.dumps(data, ensure_ascii=False, indent=1))
print("เขียน quiz-makeup-2026-11.json", list(data))
