# Tunwalai Auto Boost

Bot อัตโนมัติสำหรับโปรโมตนิยายบน Tunwalai ทุก 30 นาที ผ่าน GitHub Actions

## ฟีเจอร์

Bot ทำงาน 2 อย่างแยกกัน:

1. **กดปุ่มโปรโมต** - นิยายจะแสดงใน "นิยายที่กำลังโปรโมต"
2. **แก้ไข + บันทึก (2 รอบ)** - นิยายจะขึ้น feed "อัปเดตล่าสุด"

หมายเหตุ: ถ้าปุ่มโปรโมตอยู่ใน cooldown จะข้ามไป แต่ยังทำแก้ไข+บันทึกต่อ

## การตั้งค่า

### 1. Fork repo นี้

คลิกปุ่ม "Fork" ที่มุมขวาบน

### 2. ตั้งค่า GitHub Secrets

1. ไปที่ **Settings** → **Secrets and variables** → **Actions**
2. คลิก **New repository secret**
3. สร้าง 2 secrets:
   - `TUNWALAI_USERNAME` = email ที่ใช้ login
   - `TUNWALAI_PASSWORD` = password

### 3. เปิดใช้งาน GitHub Actions

1. ไปที่แท็บ **Actions**
2. คลิก **I understand my workflows, go ahead and enable them**

### 4. ทดสอบรัน

1. ไปที่ **Actions** → **Auto Promote & Update**
2. คลิก **Run workflow** → เลือก branch **main** → **Run workflow**
3. รอสักครู่แล้วดู log

## ตารางเวลา

Bot รันทุก 30 นาที (48 ครั้ง/วัน)

## การใช้ทรัพยากร

- GitHub Actions Free: **2,000 นาที/เดือน**
- Bot ใช้: **~1,440 นาที/เดือน** (72% ของ quota)
- แต่ละครั้งใช้เวลา: **30-60 วินาที**

## แก้ปัญหา

### ดู Log
1. **Actions** → คลิก workflow run → **promote** → **Run bot**

### ปัญหาที่พบบ่อย

**Login ไม่สำเร็จ**
- ตรวจสอบ username/password ใน Secrets

**Element not found**
- เว็บอาจเปลี่ยน HTML → ต้องแก้ selector ใน `bot.py`

**Timeout**
- เว็บช้า → Bot รอได้สูงสุด 60 วินาที ต่อ element

## ปรับแต่ง

### เปลี่ยนความถี่การรัน

แก้ไข `.github/workflows/auto-boost.yml`:
```yaml
schedule:
  - cron: '*/30 * * * *'  # ทุก 30 นาที
```

ตัวอย่าง:
- ทุก 1 ชั่วโมง: `'0 * * * *'`
- ทุก 2 ชั่วโมง: `'0 */2 * * *'`
- ทุก 15 นาที: `'*/15 * * * *'`

### แก้ Selector (ถ้าเว็บเปลี่ยน)

1. เปิด DevTools (F12) บนหน้าเว็บ
2. คลิกขวา element → Inspect
3. ดู `id`, `class`, หรือ attributes อื่นๆ
4. แก้ไขใน `bot.py`

ตัวอย่าง:
```python
# หาด้วย ID
driver.find_element(By.ID, "btnPromote")

# หาด้วย CSS Selector
driver.find_element(By.CSS_SELECTOR, "button.btn-save")

# หาด้วย Class
driver.find_element(By.CLASS_NAME, "btn-primary")
```

## โครงสร้างโปรเจกต์

```
.
├── bot.py                  # สคริปต์หลัก
├── requirements.txt        # Python dependencies
├── README.md              # คู่มือ
└── .github/workflows/
    └── auto-boost.yml     # GitHub Actions config
```

## Dependencies

- Python 3.9+
- Selenium 4.15.0
- Chrome WebDriver (ติดตั้งอัตโนมัติใน GitHub Actions)
