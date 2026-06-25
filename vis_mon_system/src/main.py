# src/main.py

import uuid
from playwright.sync_api import sync_playwright 
from config import Config
from core.scanner import ImageScanner
from pages.page_objects import LoginPage, ProductPage
from database.db_manager import ImageRepository

# uuid gen
current_test_session = str(uuid.uuid4())

def run():
    with sync_playwright() as p:
        # 1. initialize the browser in headless=False to observe the process
        browser = p.chromium.launch(headless=False) 
        context = browser.new_context()
        page = context.new_page()

        print(f"=== SESSION START : {current_test_session} ===")

        try: 
            # 2. initialize the page and authorization
            login_page = LoginPage(page)

            print(f"GOING TO THE PAGE : {Config.base_url}")
            login_page.open(Config.base_url)
            print(f"USER AUTHORIZATION : {Config.user_name}")
            login_page.login(Config.user_name, Config.user_password)

            # 3. get header_title to assert login success
            products_page = ProductPage(page)
            header_title = products_page.get_header_text()
            print(f"LOGIN SUCCESSFUL. Header title : {header_title}")

            # 4. scanning images
            # stub id's list
            target_image_ids = ("item_4_img_link", "item_0_img_link", "item_1_img_link")
            
            print(f" Scanning images by id list...")
            scanner = ImageScanner()
            scanned_results = scanner.get_image_data(page, target_image_ids)

            # 5. handling and print scanning results + DB data recording

            print("\n === SCANNING RESULTS === ")

            db_manager = ImageRepository(Config.DB_PATH)

            for img_id, img_data in scanned_results.items():
                
                # log section
                print(f"\n Element with ID : {img_id}")
                print(f"    - Name : {img_data['file_name']}")
                print(f"    - HTTP status : {img_data['status']}")
                print(f"    - Response time : {img_data['response_time_ms']} ms")

                if img_data['error_msg']:
                    print(f"    - Error : {img_data['error_msg']}")
                else:
                    print(f"    - MD5 image hash : {img_data['hash']}")
                
                # creating unique record id for each img
                unique_img_db_id = str(uuid.uuid4())

                # 6. linking the variables
                db_data = { 
                    "test_id": current_test_session, # current_test_session,
                    "file_name": img_data['file_name'],
                    "file_hash": img_data['hash'], # md5
                    "html_img_id": img_id, # img_id
                    "status": img_data['status'],
                    "response_time_ms": img_data['response_time_ms'],
                    "executed_at": img_data['executed_at'],
                    "error_msg": img_data['error_msg'],
                    "file_data": img_data['blob'], # blob
                    "file_base64_data": img_data['base64'],
                    "img_uuid": unique_img_db_id
                    }

                # 7. recording data to the DB
                db_manager.save_image(data=db_data)
                
        finally:
            # 8. closing browser
            print("\n === FINISH SESSION === ")
            browser.close()

if __name__ == "__main__":
    run()