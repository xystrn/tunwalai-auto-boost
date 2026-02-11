# Tunwalai Auto Promote Bot
# สคริปต์สำหรับกดปุ่มโปรโมตอัตโนมัติ

import os
import sys
import time
import traceback
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

# อ่าน credentials จาก environment variables
USERNAME = os.getenv('TUNWALAI_USERNAME')
PASSWORD = os.getenv('TUNWALAI_PASSWORD')

# เช็คว่ามีค่าหรือไม่
if not USERNAME or not PASSWORD:
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ERROR: ไม่พบ TUNWALAI_USERNAME หรือ TUNWALAI_PASSWORD")
    sys.exit(1)

# URLs
LOGIN_URL = "https://accounts.ookbee.com/ServiceLogin?AppCode=TUNWALAI_209&RedirectUrl=https%3A%2F%2Fwww.tunwalai.com%2FUserLogin%3FreturnUrl%3Dhttps%253A%252F%252Fwww.tunwalai.com%252F"
STORY_URL = "https://www.tunwalai.com/story/838611"

driver = None

try:
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] เริ่มต้น Tunwalai Auto Promote Bot")
    
    # ตั้งค่า Chrome options
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] กำลังตั้งค่า Chrome headless mode...")
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')

    # สร้าง WebDriver instance
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] กำลังเปิด Chrome browser...")
    driver = webdriver.Chrome(options=chrome_options)
    driver.implicitly_wait(10)
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] เปิด browser สำเร็จ")

    # เริ่มต้นการ login
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] กำลัง login...")

    # Navigate ไปยัง LOGIN_URL
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] กำลังเข้าหน้า login...")
    driver.get(LOGIN_URL)

    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] กำลังกรอก username...")
    username_field = driver.find_element(By.ID, "UserName")
    username_field.send_keys(USERNAME)

    # หา element password และกรอกค่า
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] กำลังกรอก password...")
    password_field = driver.find_element(By.ID, "Password")
    password_field.send_keys(PASSWORD)

    # หาปุ่ม submit และคลิก
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] กำลัง submit form...")
    submit_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
    submit_button.click()

    # รอ 3 วินาที
    time.sleep(3)

    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Login สำเร็จ")

    # นำทางไปหน้านิยาย
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] กำลังเข้าหน้านิยาย...")
    driver.get(STORY_URL)

    # รอ 2 วินาที
    time.sleep(2)
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] โหลดหน้านิยายสำเร็จ")

    # หาปุ่มโปรโมต
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] กำลังตรวจสอบสถานะปุ่มโปรโมต...")
    promote_button = driver.find_element(By.ID, "btnPromote")

    # เช็คว่าปุ่มมี attribute "disabled" หรือไม่
    if promote_button.get_attribute("disabled"):
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] สถานะปุ่ม: อยู่ใน cooldown (ไม่สามารถกดได้)")
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] จบการทำงาน - ข้ามการโปรโมตครั้งนี้")
        sys.exit(0)

    # คลิกปุ่ม
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] สถานะปุ่ม: พร้อมใช้งาน (สามารถกดได้)")
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] กำลังกดปุ่มโปรโมต...")
    promote_button.click()

    # รอ 3 วินาที
    time.sleep(3)

    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] โปรโมตสำเร็จ!")
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] จบการทำงาน - สำเร็จ")
    sys.exit(0)

except Exception as e:
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ERROR: เกิดข้อผิดพลาด - {e}")
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Stack trace:")
    traceback.print_exc()
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] จบการทำงาน - ล้มเหลว")
    sys.exit(1)

finally:
    # ปิด browser
    if driver:
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] กำลังปิด browser...")
        driver.quit()
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ปิด browser แล้ว")
