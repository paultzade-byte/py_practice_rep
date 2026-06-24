# src/database/db_manager.py
import sqlite3

class ImageRepository:
    def __init__(self, db_path):
        self.db_path = db_path
        self._init_db()
        # in case DB is a server 
        # then connection should be declared here 
        # self.conn = sqlite3.connect(db_path)
        # self.cursor = self.conn.cursor()

    def _init_db(self):
        # CREATE TABLE IF NOT EXIST...
        pass

    def save_image(self, data):
        """Saving the image data. data – is dictionary with parameters"""
        
        # unpacking the 'data' dictionary, it helps to avoid crashes in case of empty values
        test_id = data.get('test_id')
        file_name = data.get('file_name')
        file_hash = data.get('file_hash')
        html_img_id = data.get('html_img_id')
        file_data = data.get('file_data')
        file_base64_data = data.get('file_base64_data')
        status = data.get('status')
        response_time_ms = data.get('response_time_ms')
        executed_at = data.get('executed_at')
        error_msg = data.get('error_msg')
        img_uuid = data.get('img_uuid')

        with sqlite3.connect(self.db_path) as conn:
            conn.execute("PRAGMA foreign_keys = ON;")
            cursor = conn.cursor()

            try:
                # [1] main table record
                query_ih_meta = """
                INSERT INTO ih_meta (TEST_ID, FILE_NAME, FILE_HASH, HTML_IMG_ID, IMG_UUID) 
                VALUES (?,?,?,?,?)
                """
                #query execution and conveying parameters in the tuple
                cursor.execute(query_ih_meta, (test_id, file_name, file_hash, html_img_id, img_uuid))

                #get id from the last record
                meta_id = cursor.lastrowid

                # [2] content table record
                query_ih_content = """
                    INSERT INTO  ih_content (FILE_IH_META_ID, FILE_DATA, FILE_B64_DATA)
                    VALUES (?,?,?)
                """
                #query execution and conveying parameters in the tuple
                cursor.execute(query_ih_content, (meta_id, file_data, file_base64_data))

                # [3] logs table record
                query_ih_logs = """
                    INSERT INTO ih_logs (TEST_ID, STATUS, RESPONSE_TIME_MS, EXECUTED_AT, ERROR_MSG, FILE_IH_META_ID, IMG_UUID)
                    VALUES (?,?,?,?,?,?,?)
                """
                #query execution and conveying parameters in the tuple
                cursor.execute(query_ih_logs, (test_id, status, response_time_ms, executed_at, error_msg, meta_id, img_uuid))
                conn.commit()

            except sqlite3.IntegrityError as e:
                # Works if we violated a foreign key or unique constraint
                print(f"[Database Error] Integrity Violation: {e}")
                conn.rollback()
                return False

            except Exception as e:
                # Works for any other errors
                print(f"[Error] Something went wrong: {e}")
                conn.rollback()
                return False

        return meta_id

    def get_last_hash(self, file_name):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            query = """
            SELECT FILE_NAME, FILE_HASH 
            FROM IH_META 
            WHERE FILE_NAME = ?
            """
            cursor.execute(query, (file_name,))
            return cursor.fetchone()

    def get_last_blob(self, file_name):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            query = """
            SELECT M.FILE_NAME, C.FILE_DATA 
            FROM IH_META M 
            INNER JOIN IH_CONTENT C ON C.FILE_ID = M.ID 
            WHERE M.FILE_NAME = ?
            """
            cursor.execute(query, (file_name,))
            return cursor.fetchone()