# Tunwalai Auto Boost Bot
# สคริปต์สำหรับกดปุ่ม Boost อัตโนมัติ + แก้ไขบันทึกเพื่อขึ้น feed อัปเดตล่าสุด

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
EDIT_URL = "https://www.tunwalai.com/story/838611/edit"

driver = None

try:
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] เริ่มต้น Tunwalai Auto Boost Bot")
    
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
    
    # เช็คว่า login อยู่หรือไม่ โดยดูว่ามีปุ่มโปรโมตหรือไม่
    try:
        # ใช้ WebDriverWait รอ element สูงสุด 60 วินาที (1 นาที)
        wait = WebDriverWait(driver, 60)
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

        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] กำลังกรอก username...")
        wait = WebDriverWait(driver, 60)
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

        # รอสั้นๆ หลัง submit (3-5 วินาที)
        login_delay = random.randint(3, 5)
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] รอ {login_delay} วินาที...")
        time.sleep(login_delay)

        # ตรวจสอบว่า login สำเร็จหรือไม่ โดยเช็ค URL หรือหา element ที่แสดงว่า login แล้ว
        current_url = driver.current_url
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] URL ปัจจุบัน: {current_url}")
        
        # ถ้ายังอยู่หน้า login แสดงว่า login ไม่สำเร็จ
        if "ServiceLogin" in current_url or "login" in current_url.lower():
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ERROR: Login ไม่สำเร็จ - ยังอยู่หน้า login")
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] กรุณาตรวจสอบ username/password ใน GitHub Secrets")
            sys.exit(1)

        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Login สำเร็จ")

        # นำทางไปหน้านิยาย
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] กำลังเข้าหน้านิยาย...")
        driver.get(STORY_URL)

        # ตรวจสอบว่าอยู่หน้านิยายจริงๆ
        current_url = driver.current_url
        if "story/838611" not in current_url:
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] WARNING: ไม่ได้อยู่หน้านิยาย - URL: {current_url}")
        
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] โหลดหน้านิยายสำเร็จ")
    else:
        # ถ้า login อยู่แล้ว รอสั้นๆ (3-5 วินาที)
        story_delay = random.randint(3, 5)
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] รอ {story_delay} วินาที...")
        time.sleep(story_delay)

    # หาปุ่ม Promote
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] กำลังตรวจสอบสถานะปุ่ม Promote...")
    
    # รอสั้นๆ (3-5 วินาที) เพื่อให้ดูเป็นธรรมชาติ
    check_delay = random.randint(3, 5)
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] รอ {check_delay} วินาที...")
    time.sleep(check_delay)
    
    # ใช้ WebDriverWait รอปุ่ม Promote (สูงสุด 60 วินาที)
    wait = WebDriverWait(driver, 60)
    promote_button = wait.until(EC.presence_of_element_located((By.ID, "btnPromote")))

    # เช็คว่าปุ่มมี attribute "disabled" หรือไม่
    if promote_button.get_attribute("disabled"):
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] สถานะปุ่ม: อยู่ใน cooldown (ไม่สามารถกดได้)")
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ข้ามการ Promote ครั้งนี้")
    else:
        # คลิกปุ่ม
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] สถานะปุ่ม: พร้อมใช้งาน (สามารถกดได้)")
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] กำลังกดปุ่ม Promote...")
        
        # ลองคลิกด้วย JavaScript ถ้าคลิกปกติไม่ได้
        try:
            # รอให้ปุ่มคลิกได้
            wait.until(EC.element_to_be_clickable((By.ID, "btnPromote")))
            promote_button.click()
        except:
            # ถ้าคลิกปกติไม่ได้ ใช้ JavaScript click
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ใช้ JavaScript click...")
            driver.execute_script("arguments[0].click();", promote_button)

        # รอสั้นๆ หลังกดปุ่ม (3-5 วินาที)
        promote_delay = random.randint(3, 5)
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] รอ {promote_delay} วินาที...")
        time.sleep(promote_delay)

        # ตรวจสอบว่า Promote สำเร็จหรือไม่ โดยเช็คว่าปุ่มกลับมาเป็น disabled
        try:
            promote_button_after = driver.find_element(By.ID, "btnPromote")
            if promote_button_after.get_attribute("disabled"):
                print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ✓ ยืนยัน: ปุ่มกลับมาเป็น disabled - Promote สำเร็จแน่นอน!")
            else:
                print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] WARNING: ปุ่มยังไม่ disabled - อาจ Promote ไม่สำเร็จ")
        except:
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ไม่สามารถตรวจสอบสถานะปุ่มหลัง Promote")

        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Promote สำเร็จ!")
    
    # ========================================
    # ส่วนที่ 2: แก้ไข + บันทึก (2 รอบ) เพื่อขึ้น feed "อัปเดตล่าสุด"
    # ========================================
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] เริ่มกระบวนการแก้ไข + บันทึก (2 รอบ) เพื่อขึ้น feed อัปเดตล่าสุด...")
    
    for round_num in range(1, 3):  # ทำ 2 รอบ
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] === รอบที่ {round_num} ===")
        
        # ไปหน้าแก้ไข
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] กำลังเข้าหน้าแก้ไข...")
        driver.get(EDIT_URL)
        
        # รอสั้นๆ (3-5 วินาที)
        edit_delay = random.randint(3, 5)
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] รอ {edit_delay} วินาที...")
        time.sleep(edit_delay)
        
        # หาปุ่ม "บันทึก" และคลิก
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] กำลังหาปุ่มบันทึก...")
        wait = WebDriverWait(driver, 60)
        
        try:
            # ลองหาปุ่มบันทึก
            save_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.btn-save")))
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] กำลังกดปุ่มบันทึก...")
            
            # ลองคลิกปกติ ถ้าไม่ได้ใช้ JavaScript
            try:
                save_button.click()
            except:
                print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ใช้ JavaScript click...")
                driver.execute_script("arguments[0].click();", save_button)
            
            # รอสั้นๆ ให้ popup ขึ้นมา (2-3 วินาที)
            popup_delay = random.randint(2, 3)
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] รอ popup {popup_delay} วินาที...")
            time.sleep(popup_delay)
            
            # หาปุ่ม "ตกลง" ใน popup และคลิก
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] กำลังหาปุ่มตกลงใน popup...")
            try:
                confirm_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.btn-submit-form")))
                print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] กำลังกดปุ่มตกลง...")
                
                try:
                    confirm_button.click()
                except:
                    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ใช้ JavaScript click...")
                    driver.execute_script("arguments[0].click();", confirm_button)
                
                print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ✓ กดปุ่มตกลงสำเร็จ!")
                
                # รอให้ redirect ออกจากหน้าแก้ไข (รอสูงสุด 60 วินาที)
                print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] รอให้ redirect ออกจากหน้าแก้ไข...")
                try:
                    # รอจนกว่า URL จะไม่มีคำว่า "/edit" (แสดงว่าออกจากหน้าแก้ไขแล้ว)
                    WebDriverWait(driver, 60).until(
                        lambda d: "/edit" not in d.current_url
                    )
                    current_url = driver.current_url
                    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ✓ Redirect สำเร็จ - URL: {current_url}")
                except TimeoutException:
                    current_url = driver.current_url
                    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] WARNING: Timeout - ยังอยู่หน้าแก้ไข - URL: {current_url}")
                
                # รอสั้นๆ หลัง redirect (2-3 วินาที)
                post_redirect_delay = random.randint(2, 3)
                print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] รอ {post_redirect_delay} วินาที...")
                time.sleep(post_redirect_delay)
                
            except:
                print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] WARNING: ไม่พบปุ่มตกลง (อาจไม่มี popup)")
                # ถ้าไม่มี popup ก็รอสั้นๆ
                save_delay = random.randint(3, 5)
                time.sleep(save_delay)
            
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ✓ บันทึกรอบที่ {round_num} สำเร็จ!")
            
        except Exception as e:
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ERROR: ไม่สามารถกดปุ่มบันทึกได้ - {e}")
            # ถ้ารอบแรกล้มเหลว ยังพอทำรอบสองได้
            if round_num == 2:
                print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] WARNING: รอบที่ 2 ล้มเหลว แต่รอบที่ 1 อาจสำเร็จแล้ว")
    
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ✓ เสร็จสิ้นกระบวนการ Boost ทั้งหมด (Promote + Edit + Save 2 รอบ)!")
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] นิยายควรขึ้น feed อัปเดตล่าสุดแล้ว")
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
