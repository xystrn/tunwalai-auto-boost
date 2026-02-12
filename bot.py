# Tunwalai Auto Boost Bot
# Auto-promote stories and trigger feed updates
# Supports multiple stories with single login

import os
import sys
import time
import random
import traceback
from datetime import datetime
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

USERNAME = os.getenv('TUNWALAI_USERNAME')
PASSWORD = os.getenv('TUNWALAI_PASSWORD')
STORY_IDS_INPUT = os.getenv('STORY_IDS', '838611')

if not USERNAME or not PASSWORD:
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ERROR: Missing TUNWALAI_USERNAME or TUNWALAI_PASSWORD")
    sys.exit(1)

# Parse STORY_IDS - supports IDs or URLs
story_ids_raw = [s.strip() for s in STORY_IDS_INPUT.split(',')]
STORY_IDS = []

for story_input in story_ids_raw:
    if 'tunwalai.com/story/' in story_input:
        story_id = story_input.split('tunwalai.com/story/')[-1].split('/')[0].split('?')[0]
        STORY_IDS.append(story_id)
    else:
        STORY_IDS.append(story_input.strip())

print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Stories to boost: {len(STORY_IDS)}")
print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Story IDs: {', '.join(STORY_IDS)}")

LOGIN_URL = "https://accounts.ookbee.com/ServiceLogin?AppCode=TUNWALAI_209&RedirectUrl=https%3A%2F%2Fwww.tunwalai.com%2FUserLogin%3FreturnUrl%3Dhttps%253A%252F%252Fwww.tunwalai.com%252F"

driver = None

def process_story(driver, story_id, story_index, total_stories):
    """Process one story: Promote + Edit/Save twice"""
    print(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ========================================")
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Processing story {story_index}/{total_stories}: ID {story_id}")
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ========================================")
    
    STORY_URL = f"https://www.tunwalai.com/story/{story_id}"
    EDIT_URL = f"https://www.tunwalai.com/story/{story_id}/edit"
    
    try:
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Navigating to story page...")
        driver.get(STORY_URL)
        time.sleep(random.randint(1, 3))

        # Step 1: Click Promote button
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Checking Promote button...")
        time.sleep(random.randint(2, 4))
        
        wait = WebDriverWait(driver, 30)
        promote_button = wait.until(EC.presence_of_element_located((By.ID, "btnPromote")))

        if promote_button.get_attribute("disabled"):
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Promote button on cooldown - skipping")
        else:
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Clicking Promote button...")
            driver.execute_script("arguments[0].click();", promote_button)
            time.sleep(random.randint(2, 4))

            try:
                promote_button_after = driver.find_element(By.ID, "btnPromote")
                if promote_button_after.get_attribute("disabled"):
                    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ✓ Promote successful!")
                else:
                    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] WARNING: Promote may have failed")
            except:
                print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Cannot verify Promote status")
        
        # Step 2: Edit + Save twice
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Starting Edit + Save process (2 rounds)...")
        
        for round_num in range(1, 3):
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] --- Round {round_num} ---")
            
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Navigating to edit page...")
            driver.get(EDIT_URL)
            time.sleep(random.randint(2, 4))
            
            try:
                save_button = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "button.btn-save")))
                print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Clicking Save button...")
                driver.execute_script("arguments[0].click();", save_button)
                time.sleep(random.randint(1, 2))
                
                try:
                    confirm_button = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "button.btn-submit-form")))
                    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Clicking Confirm button...")
                    driver.execute_script("arguments[0].click();", confirm_button)
                    
                    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Waiting for redirect...")
                    try:
                        WebDriverWait(driver, 30).until(lambda d: "/edit" not in d.current_url)
                        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ✓ Redirect successful")
                    except TimeoutException:
                        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] WARNING: Timeout - still on edit page")
                    
                    time.sleep(random.randint(1, 2))
                    
                except:
                    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] WARNING: Confirm button not found")
                    time.sleep(2)
                
                print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ✓ Round {round_num} completed!")
                
            except Exception as e:
                print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ERROR: Cannot click Save button - {e}")
        
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ✓ Story {story_index}/{total_stories} completed: ID {story_id}")
        return True
        
    except Exception as e:
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ERROR: Failed to process story ID {story_id} - {e}")
        traceback.print_exc()
        return False

try:
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Starting Tunwalai Auto Boost Bot")
    
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Setting up Chrome with undetected-chromedriver...")
    chrome_options = uc.ChromeOptions()
    chrome_options.add_argument('--headless=new')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')

    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Opening Chrome browser (undetected mode)...")
    driver = uc.Chrome(options=chrome_options, use_subprocess=False)
    driver.implicitly_wait(10)
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Browser opened successfully")

    # Login once (shared session for all stories)
    print(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ========================================")
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Login Process")
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ========================================")
    
    first_story_url = f"https://www.tunwalai.com/story/{STORY_IDS[0]}"
    driver.get(first_story_url)
    
    try:
        wait = WebDriverWait(driver, 60)
        promote_button_check = wait.until(EC.presence_of_element_located((By.ID, "btnPromote")))
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ✓ Already logged in - skipping login")
        already_logged_in = True
    except (TimeoutException, NoSuchElementException):
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Not logged in - proceeding to login")
        already_logged_in = False
    
    if not already_logged_in:
        try:
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Navigating to login page...")
            driver.get(LOGIN_URL)

            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Entering username...")
            wait = WebDriverWait(driver, 60)
            username_field = wait.until(EC.presence_of_element_located((By.ID, "UserName")))
            username_field.send_keys(USERNAME)

            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Entering password...")
            password_field = wait.until(EC.presence_of_element_located((By.ID, "Password")))
            password_field.send_keys(PASSWORD)

            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Submitting form...")
            submit_button = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "button[type='submit']")))
            driver.execute_script("arguments[0].click();", submit_button)

            time.sleep(random.randint(3, 5))

            current_url = driver.current_url
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Current URL: {current_url}")
            
            if "ServiceLogin" in current_url or "login" in current_url.lower():
                print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ERROR: Login failed")
                sys.exit(1)

            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ✓ Login successful")
            
        except Exception as e:
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ERROR: Login error - {e}")
            sys.exit(1)

    # Process all stories
    print(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ========================================")
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Processing All Stories")
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ========================================")
    
    success_count = 0
    fail_count = 0
    
    for index, story_id in enumerate(STORY_IDS, start=1):
        result = process_story(driver, story_id, index, len(STORY_IDS))
        if result:
            success_count += 1
        else:
            fail_count += 1
        
        if index < len(STORY_IDS):
            between_delay = random.randint(2, 4)
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Waiting {between_delay}s before next story...")
            time.sleep(between_delay)
    
    # Summary
    print(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ========================================")
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Summary")
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ========================================")
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Total: {len(STORY_IDS)} stories")
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Success: {success_count} stories")
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Failed: {fail_count} stories")
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ✓ Completed")
    
    sys.exit(0 if fail_count == 0 else 1)

except Exception as e:
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ERROR: {e}")
    traceback.print_exc()
    sys.exit(1)

finally:
    if driver:
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Closing browser...")
        driver.quit()
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Browser closed")
