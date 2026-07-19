# src/main.py

# This module purpose is to

import uuid
from playwright.sync_api import sync_playwright 
from config import Config
from core.comparator import ImageComparator
from core.scanner import ImageScanner
from pages.page_objects import LoginPage, ProductPage
from database.db_manager import ImageRepository, ImageRepGetData

import logging
from pathlib import Path
from datetime import datetime

Path("logs").mkdir(exist_ok=True)

log_file = Path("logs")/f"vis_mon_system_log_{datetime.now():%Y-%m-%d_%H-%M-%S}.log"

logging.basicConfig(
    handlers=[
                logging.FileHandler(log_file, encoding="utf-8"),
                logging.StreamHandler()
                ],
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s: %(message)s',
    )

# uuid gen
current_test_session = str(uuid.uuid4())

def run():
    with sync_playwright() as p:
        # 1. initialize the browser in headless=False to observe the process
        browser = p.chromium.launch(headless=False) 
        context = browser.new_context()
        page = context.new_page()

        logging.info(f"=== SESSION START : {current_test_session} ===")
        try: 
            # 2. initialize the page and authorization
            login_page = LoginPage(page)

            #breakpoint()

            logging.info(f"GOING TO THE PAGE : {Config.base_url}")
            login_page.open(Config.base_url)
            logging.info(f"USER AUTHORIZATION : {Config.user_name}")
            login_page.login(Config.user_name, Config.user_password)

            # 3. get header_title to assert login success
            products_page = ProductPage(page)
            header_title = products_page.get_header_text()
            logging.info(f"LOGIN SUCCESSFUL. Header title : {header_title}")

            # 4. scanning images
            # stub id's list
            target_image_ids = ("item_4_img_link", "item_0_img_link", "item_1_img_link")

            logging.info(f" Scanning images by id list...")
            scanner = ImageScanner()
            scanned_results = scanner.get_image_data(page, target_image_ids)

            # 5. handling and print scanning results + DB data recording

            logging.info(" === SCANNING RESULTS === ")
            db_manager = ImageRepository(Config.DB_PATH)
            reader = ImageRepGetData(Config.DB_PATH)
            comparator = ImageComparator()

            for img_id, img_data in scanned_results.items():
                
                # log section
                logging.info(f" Element with ID : {img_id}")
                logging.info(f"    - Name : {img_data['file_name']}")
                logging.info(f"    - HTTP status : {img_data['status']}")
                logging.info(f"    - Response time : {img_data['response_time_ms']} ms")

                if img_data['error_msg']:
                    logging.info(f"    - Error : {img_data['error_msg']}")
                else:
                    logging.info(f"    - MD5 image hash : {img_data['hash']}")
                
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

                # 6.1
                previous_blob = reader.get_latest_blob_by_filename(img_data['file_name'])
                if previous_blob is None:
                     logging.info(
                         "    - Comparison: current ims scan is the first one"
                     )
                else:
                    result = comparator.compare(img_data['blob', previous_blob])
                    logging.info(f"    - Comparison: drift={result.drift_detected} (distance={result.visual_hamming_distance})")

                # 7. recording data to the DB
                save_result = db_manager.save_image(data=db_data)
                
                # immediate feedback
                if save_result:
                    logging.info(f"    - DB Status : Saved successfully (DB ID: {save_result})")
                else:
                    logging.info(f"    - DB Status : [!] FAILED to save in Database")
                 
        finally:
            # 8. closing browser
            logging.info(" === FINISH SESSION === ")
            browser.close()

if __name__ == "__main__":
    run()