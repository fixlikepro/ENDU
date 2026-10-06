# ENDU Quiz

ระบบทำข้อสอบของโรงเรียนเอ็นดู (ช่างซ่อมโทรศัพท์) สร้างโดย Fixlikepro

## ไฟล์

- `quiz_teacher.html` — หน้าครู สร้าง session ได้ PIN ดู dashboard real-time
- `quiz_student_pin.html` — หน้านักเรียน ใส่ PIN ทำข้อสอบ
- `admin.html` — Tibet จัดการคลังข้อสอบ (เพิ่ม/แก้/ลบ) ผ่าน UI ไม่ต้องแตะ HTML
- `migrate.html` — รันครั้งเดียวเพื่อย้ายข้อสอบเดิม (hardcoded) เข้า Firestore
- `update-basic.html` — แทนที่ข้อสอบ Basic H1 และ Basic H2 ด้วยชุดใหม่ใน `data/basic-2026-10.json` (ต้องเข้าระบบเหมือน admin.html)
- `data/` — ข้อมูลข้อสอบชุดใหม่ สคริปต์สร้าง และสำรองชุดเดิม

## Stack

Vanilla JS + Firebase (Firestore + Auth) ไม่มี build system เปิดไฟล์ในเบราว์เซอร์ใช้งานได้ทันที

## Firebase Console — สิ่งที่ Tibet ต้องตั้งก่อนใช้ admin.html

### 1. เปิด Email/Password Auth
Firebase Console → Authentication → Sign-in method → Email/Password → Enable

### 2. สร้าง user สำหรับ Tibet
Authentication → Users → Add user → กรอก email + password

### 3. Firestore Rules
Firestore → Rules → ใช้กฎนี้

```
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    // quizSets: นักเรียน/ครูอ่านได้ — admin (signed-in) เขียนได้
    match /quizSets/{setId} {
      allow read: if true;
      allow write: if request.auth != null;
    }
    // sessions: ใครๆ ก็สร้าง/อ่านได้ (ใช้ในห้องเรียน)
    match /sessions/{pin} {
      allow read, write: if true;
    }
    // results: ใครๆ ส่งได้ — แต่อ่านเฉพาะตอน list (ครูเปิดดู)
    match /results/{rid} {
      allow read, write: if true;
    }
  }
}
```

> ⚠️ Rules ของ `sessions` กับ `results` ปัจจุบันเปิดให้ทุกคน — ถ้าต้องการเข้มงวด ค่อย restrict ภายหลัง (อาจใช้ short-lived token จากครู)

### 4. รูปประกอบข้อสอบ (ไม่ใช้ Storage)

ใช้ Spark plan (ฟรี) ไม่ต้องเปิด Firebase Storage และไม่ต้องผูกบัตร

รูปประกอบข้อสอบใช้วิธี "วางลิงก์" แทน — อัปรูปขึ้นเว็บฝากรูปฟรี (เช่น imgur.com) แล้วก๊อปลิงก์มาวางในช่อง "รูปประกอบข้อนี้" ใน admin.html ระบบจะแสดงรูปจากลิงก์นั้นในข้อสอบให้นักเรียนเห็น

### 5. Migration (ครั้งเดียว)
1. ก่อน migrate ชั่วคราวเปลี่ยน `quizSets` rule เป็น `allow write: if true;`
2. เปิด `migrate.html` ใน browser → กด "เริ่ม migrate ทั้ง 4 ชุด"
3. กด "ตรวจสอบของที่อยู่บน Firestore" ดูว่าทั้ง 4 ชุดขึ้นแล้ว
4. กลับไป Firestore Rules → เปลี่ยน `quizSets` write กลับเป็น `if request.auth != null;`
5. ลบ `migrate.html` ออก หรือเก็บไว้ (Firestore ตอนนี้ block write แล้ว ถ้าไม่ login ก็เขียนไม่ได้)

## Deploy

GitHub Pages หรือ static host ใดก็ได้ — push main branch เสร็จออนไลน์

## ข้อสอบ Basic ชุดใหม่ 2026-10

ชุดใหม่ 40 ข้อ ออกจากคู่มือคอร์สระดับเบื้องต้น 5 บท แทนชุด Basic H1 (เดิม 30 ข้อ) และ Basic H2 (เดิม 20 ข้อ)

- Basic H1 20 ข้อ · โครงสร้างเครื่อง 4 · ความปลอดภัย 4 · แกะ ประกอบ เปลี่ยนอะไหล่ 9 · ราคาและร้าน 3
- Basic H2 20 ข้อ · หัวแร้ง 6 · ลมร้อน 6 · มัลติมิเตอร์ 3 · เครื่องจ่ายไฟ 4 · กล้องไมโครสโคป 1
- คำตอบถูกกระจายตำแหน่งเท่ากันทั้งสี่ตัวเลือก

วิธีเอาขึ้นใช้งาน เปิด `update-basic.html` เข้าระบบด้วยบัญชีเดียวกับ admin.html แล้วกดปุ่มแทนที่ หน้าจะดาวน์โหลดสำรองชุดเดิมให้ก่อนเขียน และแตะเฉพาะ basic1 กับ basic2 สีและเกณฑ์ผ่านคงเดิม ชุด Advance กับ Pro ไม่ถูกแตะ

แก้ข้อสอบชุดนี้ให้แก้ใน `data/build-basic-2026-10.py` แล้วรัน `python3 data/build-basic-2026-10.py` เพื่อสร้าง JSON ใหม่ หรือแก้ทีละข้อผ่าน admin.html หลังเอาขึ้นแล้ว
