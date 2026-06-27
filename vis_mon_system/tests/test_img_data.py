# tests/test_img_data.py
import os
import pytest
import sqlite3
import hashlib
import base64
from dataclasses import dataclass
from src.config import Config
from src.database.db_manager import ImageRepGetData

# the structure of context
@dataclass
class ImgTestContext:
	db: ImageRepGetData
	file_name: str
	img_uuid: str
	local_binary_img_data: bytes

@pytest.fixture(scope="module")
def ctx():
	db = ImageRepGetData(Config.DB_PATH) 	# open the DB and take the scrapped data
	file_name = 'bolt-shirt-1200x1500.c2599ac5f0a35ed5931e.jpg' # img name in the DB
	img_uuid = 'e82c5f41-2f08-4233-a4e5-3beaace62f48'

	img_path = os.path.join(Config.IMG_DIR, file_name)	# path to standard img
	with open(img_path, 'rb') as file:
		local_binary_img_data = file.read()
	
	yield ImgTestContext(db, file_name, img_uuid, local_binary_img_data) # return object
	
	# close the db connection (teardown)
	db.close()

# tests section
def test_blob(ctx):
	row_fetched  = ctx.db.get_blob(ctx.file_name, ctx.img_uuid)
	assert row_fetched["FILE_DATA"] == ctx.local_binary_img_data

def test_hash(ctx):
	row_fetched = ctx.db.get_hash(ctx.file_name, ctx.img_uuid)
	local_hash = hashlib.md5(ctx.local_binary_img_data).hexdigest()
	assert row_fetched["FILE_HASH"] == local_hash

def test_base64(ctx):
	row_fetched = ctx.db.get_base64(ctx.file_name, ctx.img_uuid)
	local_base64 = base64.b64encode(ctx.local_binary_img_data).decode('utf-8')
	assert row_fetched["FILE_B64_DATA"] == local_base64