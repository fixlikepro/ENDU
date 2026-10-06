# ENDU Quiz

ระบบทำข้อสอบของโรงเรียนเอ็นดู (ช่างซ่อมโทรศัพท์) สร้างโดย Fixlikepro

## ไฟล์

- `quiz_teacher.html` — หน้าครู สร้าง session ได้ PIN ดู dashboard real-time
- `quiz_student_pin.html` — หน้านักเรียน ใส่ PIN ทำข้อสอบ
- `admin.html` — Tibet จัดการคลังข้อสอบ (เพิ่ม/แก้/ลบ) ผ่าน UI ไม่ต้องแตะ HTML
- `migrate.html` — รันครั้งเดียวเพื่อย้ายข้อสอบเดิม (hardcoded) เข้า Firestore
- `update-quiz.html` — อัปเดตข้อสอบเป็นสามระดับตาม `data/quiz-2026-10.json` (ต้องเข้าระบบเหมือน admin.html)
- `data/` — ข้อสอบต้นฉบับใน `data/source/` สคริปต์สร้าง และสำรองของเดิม

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

## ข้อสอบสามระดับ 2026-10

จัดระดับใหม่เป็นสามระดับ ระดับละ 40 ข้อ ออกจากคู่มือคอร์สฉบับปัจจุบันของ Fixlikepro

| ชุด (doc id) | ระดับ | ที่มา |
|---|---|---|
| Basic (`basic1`) | ระดับต้น | คู่มือระดับเบื้องต้น 5 บท |
| Advance (`adv1`) | ระดับกลาง | คู่มือระดับกลาง 5 บท บทละ 8 ข้อ |
| Pro (`adv2`) | ระดับสูง | คู่มือระดับสูง 5 บท บทละ 8 ข้อ |

ชุด Basic H2 (`basic2`) รวมเข้า Basic แล้ว ตั้ง `active:false` ไว้ ไม่ลบ ผลสอบเก่ายังอยู่ คำตอบถูกกระจายตำแหน่งเท่ากันทั้งสี่ตัวเลือก

วิธีเอาขึ้นใช้งาน เปิด `update-quiz.html` เข้าระบบด้วยบัญชีเดียวกับ admin.html แล้วกดปุ่มอัปเดต หน้าจะดาวน์โหลดสำรองของเดิมทั้งหมดให้ก่อนเขียน สีและเกณฑ์ผ่านคงเดิม

แก้ข้อสอบให้แก้ใน `data/source/*.json` (คำตอบถูกอยู่ตัวเลือกแรก) แล้วรัน `python3 data/build-quiz-2026-10.py` หรือแก้ทีละข้อผ่าน admin.html หลังเอาขึ้นแล้ว สำรองของเดิมอยู่ที่ `data/backup-*.json`
