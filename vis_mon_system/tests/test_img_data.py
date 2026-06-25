# tests/test_img_data.py
import os
import pytest
import sqlite3
import hashlib
from src.config import Config
from src.database.db_manager import ImageRepGetData


@pytest.fixture(scope="module")
def test_manager():
	# open the DB and take the scrapped data
	db_manager = ImageRepGetData(Config.DB_PATH)
	# should be taken from db as last in 'count' 
	file_name = 'bolt-shirt-1200x1500.c2599ac5f0a35ed5931e.jpg'
	img_uuid = 'e82c5f41-2f08-4233-a4e5-3beaace62f48'
	return db_manager, file_name, img_uuid

def test_blob(test_manager):
	# unpacking the return fron the fixture
	db_manager, file_name, img_uuid = test_manager
	row_fetched  = db_manager.get_blob(file_name, img_uuid)
	blob_fetched = row_fetched["FILE_DATA"]

	img_path = os.path.join(Config.IMG_DIR, file_name)
	with open(img_path, 'rb') as file:
		local_blob = file.read()
		assert blob_fetched == local_blob

def test_hash(test_manager):
	# unpacking the return fron the fixture
	db_manager, file_name, img_uuid = test_manager
	row_fetched = db_manager.get_hash(file_name, img_uuid)
	hash_fetched = row_fetched["FILE_HASH"]

	img_path = os.path.join(Config.IMG_DIR, file_name)
	hasher = hashlib.md5()

	with open(img_path, 'rb') as file:
		while chunk := file.read(4096):
			hasher.update(chunk)
	
	local_hash = hasher.hexdigest()

	assert hash_fetched == local_hash

def test_base64(test_manager):
	pass
