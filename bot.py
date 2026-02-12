# Tunwalai Auto Promote Bot
# สคริปต์สำหรับกดปุ่มโปรโมตอัตโนมัติ

import os
import sys
import time
import random
import traceback
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementNotInteractableException

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
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] กำลังตรวจสอบสถานะ login...")

    # ไปที่หน้านิยายก่อนเพื่อเช็คว่า login อยู่หรือไม่
    driver.get(STORY_URL)
    
    # รอให้หน้าโหลด (15-30 วินาที)
    initial_delay = random.randint(15, 30)
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] รอหน้าเว็บโหลด {initial_delay} วินาที...")
    time.sleep(initial_delay)
    
    # เช็คว่า login อยู่หรือไม่ โดยดูว่ามีปุ่มโปรโมตหรือไม่
    try:
        # ใช้ WebDriverWait รอ element สูงสุด 20 วินาที
        wait = WebDriverWait(driver, 20)
        promote_button_check = wait.until(EC.presence_of_element_located((By.ID, "btnPromote")))
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ตรวจพบว่า login อยู่แล้ว - ข้ามขั้นตอน login")
        already_logged_in = True
    except (TimeoutException, NoSuchElementException):
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ยังไม่ได้ login - จะทำการ login")
        already_logged_in = False
    
    # ถ้ายังไม่ได้ login ให้ไป login
    if not already_logged_in:
        # Navigate ไปยัง LOGIN_URL
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] กำลังเข้าหน้า login...")
        driver.get(LOGIN_URL)
        
        # รอหน้า login โหลด (15-25 วินาที)
        login_page_delay = random.randint(15, 25)
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] รอหน้า login โหลด {login_page_delay} วินาที...")
        time.sleep(login_page_delay)

        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] กำลังกรอก username...")
        wait = WebDriverWait(driver, 20)
        username_field = wait.until(EC.presence_of_element_located((By.ID, "UserName")))
        username_field.send_keys(USERNAME)

        # หา element password และกรอกค่า
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] กำลังกรอก password...")
        password_field = wait.until(EC.presence_of_element_located((By.ID, "Password")))
        password_field.send_keys(PASSWORD)

        # หาปุ่ม submit และคลิก
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] กำลัง submit form...")
        submit_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']")))
        submit_button.click()

        # รอให้ login เสร็จ (15-30 วินาที เพื่อรอหน้าเว็บโหลด)
        login_delay = random.randint(15, 30)
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] รอ {login_delay} วินาที...")
        time.sleep(login_delay)

        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Login สำเร็จ")

        # นำทางไปหน้านิยาย
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] กำลังเข้าหน้านิยาย...")
        driver.get(STORY_URL)

        # รอให้หน้านิยายโหลด (15-40 วินาที)
        story_delay = random.randint(15, 40)
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] รอ {story_delay} วินาที...")
        time.sleep(story_delay)
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] โหลดหน้านิยายสำเร็จ")
    else:
        # ถ้า login อยู่แล้ว รอสักหน่อยเพื่อให้หน้าโหลดเสร็จ
        story_delay = random.randint(15, 25)
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] รอ {story_delay} วินาที...")
        time.sleep(story_delay)

    # หาปุ่มโปรโมต
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] กำลังตรวจสอบสถานะปุ่มโปรโมต...")
    
    # รอสุ่มก่อนหาปุ่ม (15-30 วินาที) เพื่อให้ดูเป็นธรรมชาติ
    check_delay = random.randint(15, 30)
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] รอ {check_delay} วินาที...")
    time.sleep(check_delay)
    
    # ใช้ WebDriverWait รอปุ่มโปรโมต
    wait = WebDriverWait(driver, 20)
    promote_button = wait.until(EC.presence_of_element_located((By.ID, "btnPromote")))

    # เช็คว่าปุ่มมี attribute "disabled" หรือไม่
    if promote_button.get_attribute("disabled"):
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] สถานะปุ่ม: อยู่ใน cooldown (ไม่สามารถกดได้)")
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] จบการทำงาน - ข้ามการโปรโมตครั้งนี้")
        sys.exit(0)

    # คลิกปุ่ม
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] สถานะปุ่ม: พร้อมใช้งาน (สามารถกดได้)")
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] กำลังกดปุ่มโปรโมต...")
    
    # ลองคลิกด้วย JavaScript ถ้าคลิกปกติไม่ได้
    try:
        # รอให้ปุ่มคลิกได้
        wait.until(EC.element_to_be_clickable((By.ID, "btnPromote")))
        promote_button.click()
    except:
        # ถ้าคลิกปกติไม่ได้ ใช้ JavaScript click
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ใช้ JavaScript click...")
        driver.execute_script("arguments[0].click();", promote_button)

    # รอให้โปรโมตเสร็จ (15-40 วินาที)
    promote_delay = random.randint(15, 40)
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] รอ {promote_delay} วินาที...")
    time.sleep(promote_delay)

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
