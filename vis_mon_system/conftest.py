import pytest
from src.config import Config
from src.pages.page_objects import LoginPage, ProductPage, NeverPage, Cart

@pytest.fixture
def test_login(page):
    login_page = LoginPage(page)
    login_page.open(Config.base_url)
    return login_page

@pytest.fixture
def test_manager(page, test_login):
    """Default function-scoped fixture."""
    test_login.login(Config.user_name, Config.user_password)
    return ProductPage(page)

@pytest.fixture
def test_never_page(page):
    """Distinct page for 404 test"""
    never_page = NeverPage(page)
    return never_page.open_wrong_page(Config.base_url)

@pytest.fixture
def test_cart(page, test_login):
    test_login.login(Config.user_name, Config.user_password)
    return Cart(page)