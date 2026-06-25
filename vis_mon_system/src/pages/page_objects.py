# src/pages/page_objects.py

class LoginPage:
    def __init__(self, page):
        self.page = page
        self.name_input = page.locator("input[name='user-name']")
        self.password_input = page.locator("input[name='password']")
        self.submit_btn = page.locator("input[name='login-button']")
        self.error_msg = page.locator(".error-message-container")

    # opening the page
    def open(self, url):
        self.page.goto(url)

    # login
    def login(self, username, password):
        self.name_input.fill(username)
        self.password_input.fill(password)
        self.submit_btn.click()

    # for case with error
    def get_error_text(self):
        return self.error_msg.text_content()

class ProductPage:
    def __init__ (self, page):
        self.page = page
        self.product_header = page.locator(".title")
        self.main_menu_btn = page.locator(".bm-burger-button")
        self.img_locators = page.locator(".inventory_item")

        # seeking for product card by text inside of container
        self.backpack_item = page.locator(".inventory_item").filter(has_text="Sauce Labs Backpack")

    def get_header_text(self):
        return self.product_header.text_content()

    def open_menu(self):
        return self.main_menu_btn.click()

    def get_prod_count(self):
        return self.img_locators.count()