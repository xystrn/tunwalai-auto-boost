# Tunwalai Auto Promote Bot

Bot สำหรับกดปุ่มโปรโมตนิยายบน Tunwalai อัตโนมัติทุก 2 ชั่วโมง โดยใช้ Python + Selenium รันผ่าน GitHub Actions

## การตั้งค่า

### 1. Fork repo นี้ไปยัง GitHub account ของคุณ

คลิกปุ่ม "Fork" ที่มุมขวาบนของหน้า repo

### 2. ตั้งค่า GitHub Secrets

GitHub Secrets ใช้เก็บข้อมูลที่เป็นความลับ (username และ password) อย่างปลอดภัย

ขั้นตอน:
1. ไปที่ repo ที่ fork มาแล้ว
2. คลิก **Settings** (แท็บด้านบน)
3. ในเมนูด้านซ้าย คลิก **Secrets and variables** → **Actions**
4. คลิกปุ่ม **New repository secret**
5. สร้าง secret ตัวแรก:
   - Name: `TUNWALAI_USERNAME`
   - Secret: ใส่ username ของคุณ (email ที่ใช้ login)
   - คลิก **Add secret**
6. สร้าง secret ตัวที่สอง:
   - Name: `TUNWALAI_PASSWORD`
   - Secret: ใส่ password ของคุณ
   - คลิก **Add secret**

หมายเหตุ: Secrets จะถูกเข้ารหัสและไม่สามารถดูได้หลังจากบันทึกแล้ว

### 3. เปิดใช้งาน GitHub Actions

GitHub Actions จะไม่ทำงานอัตโนมัติใน forked repo จนกว่าจะเปิดใช้งาน

ขั้นตอน:
1. ไปที่แท็บ **Actions** (แท็บด้านบน)
2. คลิกปุ่ม **I understand my workflows, go ahead and enable them**
3. คลิกที่ workflow **Auto Promote** ในรายการด้านซ้าย
4. คลิกปุ่ม **Enable workflow** (ถ้ามี)

### 4. ทดสอบรัน workflow

ก่อนรอให้ bot รันอัตโนมัติ ควรทดสอบก่อนว่าทำงานได้

ขั้นตอน:
1. ไปที่แท็บ **Actions**
2. คลิกที่ workflow **Auto Promote** ในรายการด้านซ้าย
3. คลิกปุ่ม **Run workflow** (ปุ่มสีน้ำเงิน)
4. เลือก branch **main** (หรือ branch หลักของคุณ)
5. คลิก **Run workflow** สีเขียว
6. รอสักครู่ workflow จะเริ่มทำงาน (refresh หน้าถ้าไม่เห็น)

### 5. ดู log และตรวจสอบผลลัพธ์

Log จะแสดงรายละเอียดการทำงานของ bot ในแต่ละครั้ง

ขั้นตอนดู log:
1. ไปที่แท็บ **Actions**
2. คลิกที่ workflow run ที่ต้องการดู (จะแสดงเป็นรายการพร้อม timestamp)
3. คลิกที่ job **promote** (จะเห็นสีเขียวถ้าสำเร็จ สีแดงถ้าล้มเหลว)
4. คลิกที่ step **Run bot** เพื่อดู log รายละเอียด

ตัวอย่าง log เมื่อสำเร็จ:
```
เริ่มต้น bot...
กำลัง login...
Login สำเร็จ
กำลังเข้าหน้านิยาย...
กำลังกดปุ่มโปรโมต...
โปรโมตสำเร็จ!
ปิด browser แล้ว
```

ตัวอย่าง log เมื่อปุ่มอยู่ใน cooldown:
```
เริ่มต้น bot...
กำลัง login...
Login สำเร็จ
กำลังเข้าหน้านิยาย...
ปุ่มอยู่ใน cooldown - ข้ามไป
ปิด browser แล้ว
```

ตัวอย่าง log เมื่อเกิด error:
```
เริ่มต้น bot...
ERROR: ไม่พบ TUNWALAI_USERNAME หรือ TUNWALAI_PASSWORD
```

## โครงสร้างโปรเจกต์

```
.
├── bot.py                  # สคริปต์หลัก
├── requirements.txt        # Python dependencies
├── README.md              # คู่มือการใช้งาน
├── .gitignore             # ไฟล์ที่ไม่ต้อง commit
└── .github/
    └── workflows/
        └── promote.yml    # GitHub Actions workflow
```

## Dependencies

- Python 3.9 หรือสูงกว่า
- Selenium 4.15.0
- Chrome WebDriver (ติดตั้งอัตโนมัติใน GitHub Actions)

## หมายเหตุการใช้ทรัพยากร

### GitHub Actions Free Tier
- GitHub Actions Free มี **2,000 นาที/เดือน** สำหรับ public repositories
- แต่ละครั้งที่ bot รันใช้เวลาประมาณ **30-60 วินาที**
- Bot รันทุก 2 ชั่วโมง = **12 ครั้ง/วัน** = **360 ครั้ง/เดือน**
- เวลาที่ใช้ทั้งหมด ≈ **360 ครั้ง × 1 นาที = 360 นาที/เดือน**
- **เพียงพอสำหรับการใช้งาน** (ใช้ประมาณ 18% ของ quota)

### ตารางเวลาการรัน
Bot จะรันอัตโนมัติตามเวลา UTC ทุก 2 ชั่วโมง:
- 00:00, 02:00, 04:00, 06:00, 08:00, 10:00, 12:00, 14:00, 16:00, 18:00, 20:00, 22:00 UTC

แปลงเป็นเวลาไทย (UTC+7):
- 07:00, 09:00, 11:00, 13:00, 15:00, 17:00, 19:00, 21:00, 23:00, 01:00, 03:00, 05:00

### พฤติกรรมเมื่อปุ่มอยู่ใน cooldown
- ถ้าปุ่มโปรโมตยังอยู่ใน cooldown (ไม่สามารถกดได้) bot จะข้ามไปโดยไม่ถือว่าเป็น error
- Workflow จะแสดงสถานะสีเขียว (success) แม้ว่าจะไม่ได้กดปุ่ม
- สามารถดูใน log ว่าข้ามไปเพราะ cooldown หรือกดปุ่มสำเร็จ

### การปรับเปลี่ยนความถี่
ถ้าต้องการเปลี่ยนความถี่การรัน แก้ไขไฟล์ `.github/workflows/promote.yml`:
```yaml
schedule:
  - cron: '0 */2 * * *'  # ทุก 2 ชั่วโมง
```

ตัวอย่าง:
- ทุก 3 ชั่วโมง: `'0 */3 * * *'`
- ทุก 4 ชั่วโมง: `'0 */4 * * *'`
- ทุก 6 ชั่วโมง: `'0 */6 * * *'`

## แก้ไข Selectors (ถ้าหน้าเว็บเปลี่ยน)

ถ้าหน้าเว็บ Tunwalai มีการเปลี่ยนแปลง HTML structure และ bot ไม่ทำงาน คุณอาจต้องแก้ไข selectors

### วิธีหา selector ใหม่

1. **เปิดหน้าเว็บที่ต้องการตรวจสอบ**
   - หน้า login: https://accounts.ookbee.com/ServiceLogin?AppCode=TUNWALAI_209&...
   - หน้านิยาย: https://www.tunwalai.com/story/838611

2. **เปิด Developer Tools**
   - กด **F12** หรือคลิกขวาแล้วเลือก "Inspect"

3. **เลือก element ที่ต้องการ**
   - กด **Ctrl+Shift+C** (หรือคลิกไอคอน pointer ใน DevTools)
   - คลิกที่ element บนหน้าเว็บ (เช่น ช่อง username, ปุ่มโปรโมต)

4. **ดู HTML attributes**
   - ดูที่ HTML code ที่ highlight อยู่
   - มองหา attributes เช่น `id`, `name`, `class`, `type`

5. **แก้ไขใน bot.py**
   - เปิดไฟล์ `bot.py`
   - แก้ไข selector ตามที่พบ

### Selectors ปัจจุบัน

**หน้า Login (accounts.ookbee.com):**
```python
# ช่อง username
username_field = driver.find_element(By.ID, "UserName")

# ช่อง password
password_field = driver.find_element(By.ID, "Password")

# ปุ่ม submit
submit_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
```

**หน้านิยาย (tunwalai.com):**
```python
# ปุ่มโปรโมต
promote_button = driver.find_element(By.ID, "btnPromote")
```

### ตัวอย่างการแก้ไข

ถ้า element เปลี่ยนจาก `id="UserName"` เป็น `id="username"`:
```python
# เดิม
username_field = driver.find_element(By.ID, "UserName")

# แก้เป็น
username_field = driver.find_element(By.ID, "username")
```

ถ้า element ไม่มี id แต่มี class:
```python
# ใช้ class แทน
username_field = driver.find_element(By.CLASS_NAME, "login-username")

# หรือใช้ CSS selector
username_field = driver.find_element(By.CSS_SELECTOR, ".login-username")
```

ถ้า element มี name attribute:
```python
username_field = driver.find_element(By.NAME, "username")
```

### วิธีทดสอบหลังแก้ไข

1. Commit และ push การเปลี่ยนแปลง
2. ไปที่ Actions → Run workflow เพื่อทดสอบ
3. ดู log เพื่อตรวจสอบว่าทำงานได้

### Selenium Locator Strategies

| Strategy | ตัวอย่าง | เมื่อไหร่ควรใช้ |
|----------|---------|-----------------|
| `By.ID` | `By.ID, "btnPromote"` | เมื่อ element มี id (แนะนำ - เร็วและแม่นยำ) |
| `By.NAME` | `By.NAME, "username"` | เมื่อ element มี name attribute |
| `By.CLASS_NAME` | `By.CLASS_NAME, "btn-primary"` | เมื่อ element มี class (ระวังถ้ามีหลาย element) |
| `By.CSS_SELECTOR` | `By.CSS_SELECTOR, "button[type='submit']"` | สำหรับ selector ที่ซับซ้อน |
| `By.XPATH` | `By.XPATH, "//button[@id='btnPromote']"` | เมื่อต้องการความยืดหยุ่นสูง |

### การแก้ปัญหาทั่วไป

**ปัญหา: Element not found**
- ลอง เพิ่ม `time.sleep(2)` ก่อนหา element เพื่อรอให้หน้าโหลด
- ตรวจสอบว่า selector ถูกต้อง

**ปัญหา: Element not clickable**
- ลองเพิ่ม `time.sleep(1)` ก่อนคลิก
- ตรวจสอบว่า element ไม่ถูกบังโดย element อื่น

**ปัญหา: Login ไม่สำเร็จ**
- ตรวจสอบว่า secrets ถูกตั้งค่าถูกต้อง
- ตรวจสอบว่า username/password ยังใช้งานได้
