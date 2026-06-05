# ENDU Quiz

ระบบทำข้อสอบของโรงเรียนเอ็นดู (ช่างซ่อมโทรศัพท์) สร้างโดย Fixlikepro

## ไฟล์

- `quiz_teacher.html` — หน้าครู สร้าง session ได้ PIN ดู dashboard real-time
- `quiz_student_pin.html` — หน้านักเรียน ใส่ PIN ทำข้อสอบ
- `admin.html` — Tibet จัดการคลังข้อสอบ (เพิ่ม/แก้/ลบ) ผ่าน UI ไม่ต้องแตะ HTML
- `migrate.html` — รันครั้งเดียวเพื่อย้ายข้อสอบเดิม (hardcoded) เข้า Firestore

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

### 4. Firebase Storage (สำหรับรูปประกอบข้อสอบ)

Firebase Console → Storage → Get started → Production mode

Storage Rules

```
rules_version = '2';
service firebase.storage {
  match /b/{bucket}/o {
    match /quiz-images/{allPaths=**} {
      allow read: if true;
      allow write: if request.auth != null;
    }
  }
}
```

### 5. Migration (ครั้งเดียว)
1. ก่อน migrate ชั่วคราวเปลี่ยน `quizSets` rule เป็น `allow write: if true;`
2. เปิด `migrate.html` ใน browser → กด "เริ่ม migrate ทั้ง 4 ชุด"
3. กด "ตรวจสอบของที่อยู่บน Firestore" ดูว่าทั้ง 4 ชุดขึ้นแล้ว
4. กลับไป Firestore Rules → เปลี่ยน `quizSets` write กลับเป็น `if request.auth != null;`
5. ลบ `migrate.html` ออก หรือเก็บไว้ (Firestore ตอนนี้ block write แล้ว ถ้าไม่ login ก็เขียนไม่ได้)

## Deploy

GitHub Pages หรือ static host ใดก็ได้ — push main branch เสร็จออนไลน์
