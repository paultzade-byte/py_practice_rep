# tests/test_ui.py
import pytest
import sqlite3
from src.config import Config
from src.pages.page_objects import ProductPage, LoginPage

@pytest.fixture
def test_manager(page):
	login_page = LoginPage(page)
	login_page.open(Config.base_url)
	login_page.login(Config.user_name, Config.user_password)

    # get header_title to assert login success
	products_page = ProductPage(page)
	return products_page

def test_count(test_manager):
	actual_count = test_manager.get_prod_count()
	assert actual_count == 6

def test_assert_header(test_manager):
	header_title = test_manager.get_header_text()
	assert header_title == "Products"
