# ENDU Quiz

ระบบทำข้อสอบของโรงเรียนเอ็นดู (ช่างซ่อมโทรศัพท์) สร้างโดย Fixlikepro

## ไฟล์

- `quiz_teacher.html` — หน้าครู สร้าง session ได้ PIN ดู dashboard real-time
- `quiz_student_pin.html` — หน้านักเรียน ใส่ PIN ทำข้อสอบ
- `admin.html` — Tibet จัดการคลังข้อสอบ (เพิ่ม/แก้/ลบ) ผ่าน UI ไม่ต้องแตะ HTML

## Stack

Vanilla JS + Firebase Firestore (realtime) + Firebase Storage (รูปข้อสอบ) ไม่มี build system เปิดไฟล์ในเบราว์เซอร์ใช้งานได้ทันที

## Deploy

GitHub Pages หรือ static host ใดก็ได้ — push main branch เสร็จออนไลน์
