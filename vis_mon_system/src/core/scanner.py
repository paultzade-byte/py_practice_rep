# src/core/scanner.py
import base64 # для більшої швидкості варто встановити та імпортувати pybase64
import hashlib
import time 
from datetime import datetime

class ImageScanner:
    @staticmethod
    def get_image_data(page, image_ids: tuple) -> dict:
        """
        Takes the active page object and an ID tuple. 
        Returns a dictionary with image data
        """
        results = {}

        for img_id in image_ids:
            try:
                # seeking an image
                image_locator = page.locator(f"#{img_id} img") # looking for img inside element with id=img_id
                image_locator.wait_for(state="attached", timeout=5000)

                # get absolute (full) URL of image
                image_url = image_locator.evaluate("node => node.src")
                print(f"[{img_id}] found URL: {image_url}")

                # take the image name
                file_name = image_url.split('/')[-1]
                if not file_name:
                    file_name = f"unknown_{img_id}.png"

                # downloaling an original file
                start_time = time.time()
                response = page.context.request.get(image_url)
                end_time = time.time()

                # metrics collection
                status_code = response.status 
                response_time_ms = int((end_time - start_time) * 1000)
                executed_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S") 

                # handling unsuccessful status
                if not response.ok:
                    results[img_id] = {
                        "file_name": file_name,
                        "status": status_code,
                        "response_time_ms": response_time_ms,
                        "executed_at": executed_at,
                        "error_msg": f"HTTP Error {status_code}",
                        "html_img_id": img_id
                    }
                    continue

                # handling successful status

                #    image in the string format
                file_blob_data = response.body() # get BLOB
                file_base64_data = base64.b64encode(file_blob_data).decode('utf-8') # get base64
                file_hash_data = hashlib.md5(file_blob_data).hexdigest() # get hash md5

                #    return full dictionary
                results[img_id] = {
                    "file_name": file_name,
                    "blob": file_blob_data,
                    "base64": file_base64_data,
                    "hash": file_hash_data,
                    "status": str(status_code), # DB waits for TEXT for STATUS
                    "response_time_ms": response_time_ms,
                    "executed_at": executed_at, 
                    "error_msg": None
                }

            except Exception as e:
                # handling critical errors(element not found etc.)
                print(f"[{img_id}] Fail to process: {e}")
                results[img_id] = {
                    "file_name": f"failed_{img_id}",
                    "status": "FAIL",
                    "response_time_ms": 0,
                    "executed_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "error_msg": str(e),  # we don't need to crash whole test even if one image downloading will fail   
                    "html_img_id": img_id
                    }

        return results