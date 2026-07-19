# src/database/db_manager.py

import sqlite3
from dataclasses import dataclass
from typing import Any
from pathlib import Path

# next 11 rows allow us to write received data into variables and convey this variables to test modules
@dataclass
class Base64Result:
    file_base64_data: str

@dataclass
class HashResult:
    file_hash: str

@dataclass
class BlobResult:
    file_data: bytes

# write data into db
class ImageRepository:
    def __init__(self, db_path: str) -> None:
        self.db_path = db_path
        self._init_db()
        # in case DB is a server 
        # then connection should be declared here 
        # self.conn = sqlite3.connect(db_path)
        # self.cursor = self.conn.cursor()

    def _init_db(self) -> None:
        schema_path = Path(__file__)/"scehma.sql"
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("PRAGMA foreign_keys = ON;")
            conn.executescript(schema_path.read_text())

    def save_image(self, data: dict[str, Any]) -> int | bool:
        """Saving the image data. data – is dictionary with parameters"""
        
        # unpacking the 'data' dictionary
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

        # fast cheknig for None values
        required = {
            'test_id': test_id,
            'file_name': file_name,
            'file_hash': file_hash,
            'file_data': file_data,
            'file_base64_data': file_base64_data
        }
        missing = [key for key, value in required.items() if value is None]
        if missing:
            raise ValueError(f"Missing requirel fields: {missing}")

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
                if meta_id is None:
                    conn.rollback()
                    return False       

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

# read data from db
class ImageRepGetData:
    def __init__(self, db_path: str) -> None:
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
        # (before cursor)row factory returns each row in immutable dictionary format ("collumn_name": "value")
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()

    def get_hash(self, file_name: str, img_uuid: str) -> HashResult | None:
        query = """
        SELECT FILE_NAME, FILE_HASH 
        FROM IH_META 
        WHERE FILE_NAME = ? AND IMG_UUID = ?
        """
        self.cursor.execute(query, (file_name, img_uuid))
        row = self.cursor.fetchone()

        if row:
            return HashResult(file_hash=row["FILE_HASH"])
        return None

    def get_blob(self, file_name: str, img_uuid: str) -> BlobResult | None:
        query = """
        SELECT M.FILE_NAME, C.FILE_DATA 
        FROM IH_META M 
        INNER JOIN IH_CONTENT C ON C.FILE_IH_META_ID = M.ID 
        WHERE M.FILE_NAME = ? AND M.IMG_UUID = ?
        """
        self.cursor.execute(query, (file_name, img_uuid))
        row = self.cursor.fetchone()

        if row:
            return BlobResult(file_data=row["FILE_DATA"])
        return None

    def get_base64(self, file_name: str, img_uuid: str) -> Base64Result | None:
        query = """
        SELECT M.FILE_NAME, C.FILE_B64_DATA 
        FROM IH_META M 
        INNER JOIN IH_CONTENT C ON C.FILE_IH_META_ID = M.ID
        WHERE M.FILE_NAME = ? AND M.IMG_UUID = ?
        """
        self.cursor.execute(query, (file_name, img_uuid))
        row = self.cursor.fetchone()

        if row:
            return Base64Result(file_base64_data=row["FILE_B64_DATA"])
        return None

    def get_latest_blob_by_filename(self, file_name: str):
        query = """
                SELECT ih_content.FILE_DATA
                FROM ih_meta
                JOIN ih_content ON ih_content.FILE_IH_META_ID = ih_meta.ID
                WHERE ih_meta.FILE_NAME = ?
                ORDER BY ih_meta.ID DESC LIMIT 1 \
                """
        row = self.conn.execute(query, (file_name,)).fetchone()
        return row[0] if row else None

    def close(self) -> None:
        self.conn.close()