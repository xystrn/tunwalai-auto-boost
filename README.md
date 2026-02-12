# Tunwalai Auto Boost

Bot อัตโนมัติสำหรับ Boost นิยายบน Tunwalai ทุก 1 ชั่วโมง ผ่าน GitHub Actions (ฟรี)

## Bot ทำอะไร?

1. **กดปุ่ม Promote** - นิยายขึ้น "นิยายที่กำลังโปรโมต"
2. **แก้ไข + บันทึก 2 รอบ** - นิยายขึ้น feed "อัปเดตล่าสุด"

## วิธีใช้

### 1. Fork repo นี้
คลิกปุ่ม "Fork" ที่มุมขวาบน

### 2. ตั้งค่า Secrets
1. ไปที่ **Settings** → **Secrets and variables** → **Actions**
2. คลิก **New repository secret** แล้วสร้าง 2 ตัว:
   - `TUNWALAI_USERNAME` = email ที่ใช้ login
   - `TUNWALAI_PASSWORD` = password

### 3. เปิดใช้งาน Actions
1. ไปที่แท็บ **Actions**
2. คลิก **I understand my workflows, go ahead and enable them**

### 4. ทดสอบ
1. ไปที่ **Actions** → **Auto Promote & Update**
2. คลิก **Run workflow** → **Run workflow**
3. ดู log ว่าทำงานสำเร็จหรือไม่

## ตารางเวลา

รันทุก 1 ชั่วโมง (24 ครั้ง/วัน)

## การใช้ทรัพยากร

- GitHub Actions Free: 2,000 นาที/เดือน
- Bot ใช้: ~120 นาที/เดือน (6% ของ quota)
- แต่ละครั้งใช้เวลา: 2-3 นาที

## เปลี่ยนความถี่

แก้ไข `.github/workflows/auto-boost.yml`:

```yaml
schedule:
  - cron: '19 * * * *'  # รันทุกชั่วโมงตรงนาทีที่ 19
```

ตัวอย่าง:
- ทุก 2 ชั่วโมง: `'0 */2 * * *'`
- ทุก 30 นาที: `'*/30 * * * *'`

## แก้ปัญหา

**ดู Log**: Actions → คลิก workflow run → promote → Run bot

**Login ไม่สำเร็จ**: ตรวจสอบ username/password ใน Secrets

**Element not found**: เว็บเปลี่ยน HTML → แก้ selector ใน `bot.py`
