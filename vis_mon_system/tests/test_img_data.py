# tests/test_img_data.py
import os
import uuid
import hashlib
import base64
from dataclasses import dataclass
from typing import Iterator

import pytest

from src.config import Config
from src.database.db_manager import ImageRepGetData, ImageRepository

# the structure of context
@dataclass
class ImgTestContext:
	db: ImageRepGetData
	file_name: str
	img_uuid: str
	local_binary_img_data: bytes

# arranging environment for test run

#tmp_path is a builtin pytest fixture (means that pytest automatically create temp folder, return path (Path object) )
@pytest.fixture
def ctx(tmp_path) -> Iterator[ImgTestContext]:
	"""
	An isolated DB for each test
	:param tmp_path:
	:return:
	"""
	db_path = str(tmp_path/"test_ih.sqlite3") 	# open the DB and take the scrapped data
	file_name = 'bolt-shirt-1200x1500.c2599ac5f0a35ed5931e.jpg' # img name in the DB
	#img_uuid = 'e82c5f41-2f08-4233-a4e5-3beaace62f48'

	img_path = os.path.join(Config.IMG_DIR, file_name)	# path to standard img
	with open(img_path, 'rb') as file:
		local_binary_img_data = file.read()

	img_uuid = str(uuid.uuid4())

	writer = ImageRepository(db_path)
	writer.save_image({
		"test_id": "test-session",
		"file_name": file_name,
		"file_hash": hashlib.md5(local_binary_img_data).hexdigest(),
		"html_img_id": "item_0_img_link",
		"file_data": local_binary_img_data,
		"file_base64_data": base64.b64encode(local_binary_img_data).decode("utf-8"),
		"status": "200",
		"response_time_ms": 42,
		"executed_at": "2026-07-17 12:00:00",
		"error_msg": None,
		"img_uuid": img_uuid,
	})

	reader = ImageRepGetData(db_path)
	yield ImgTestContext(reader, file_name, img_uuid, local_binary_img_data) # return object
	# close the db connection (teardown)
	reader.close()

# tests section
# hapy path write -> read round-trip
def test_blob(ctx: ImgTestContext):
	row_fetched  = ctx.db.get_blob(ctx.file_name, ctx.img_uuid)
	assert row_fetched is not None
	assert row_fetched.file_data == ctx.local_binary_img_data

def test_hash(ctx: ImgTestContext):
	row_fetched = ctx.db.get_hash(ctx.file_name, ctx.img_uuid)
	assert row_fetched is not None
	assert row_fetched.file_hash == hashlib.md5(ctx.local_binary_img_data).hexdigest() #local_hash

def test_base64(ctx: ImgTestContext):
	row_fetched = ctx.db.get_base64(ctx.file_name, ctx.img_uuid)
	assert row_fetched is not None
	assert row_fetched.file_base64_data == base64.b64encode(ctx.local_binary_img_data).decode('utf-8')

# edge cases
def test_get_blab_returns_none_for_unknown_uuid(ctx: ImgTestContext):
	"""Reading an unknown record shouldn't fall but silently return None"""
	row = ctx.reader.get_blob(ctx.file_name, str(uuid.uuid4()))
	assert row is None

def test_save_image_rejects_duslicate_uuid(ctx: ImgTestContext,tmp_path):
	"""IMG_UUID is unique. The 2nd insert with the same uuid should fall
	in IntegrityError. Do rollback and return False but don't return half of data (meta without content)."""
	writer = ImageRepository(str(tmp_path / "dup_test.sqlite3"))
	payload = {
		"test_id": "dup-session",
        "file_name": ctx.file_name,
        "file_hash": hashlib.md5(ctx.local_binary_img_data).hexdigest(),
        "html_img_id": "item_0_img_link",
        "file_data": ctx.local_binary_img_data,
        "file_base64_data": base64.b64encode(ctx.local_binary_img_data).decode("utf-8"),
        "status": "200",
        "response_time_ms": 42,
        "executed_at": "2026-07-17 12:00:00",
        "error_msg": None,
        "img_uuid": "fixed-uuid-for-duplicate-test",
	}
	first = writer.save_image(payload)
	assert first is not False

	second = writer.save_image(payload)
	assert second is False