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
        self.main_menu_btn.click()
        return ProductPage(self.page)

    def get_prod_count(self):
        return self.img_locators.count()


class Cart:
    def __init__(self, page):
        self.page = page
        self.add_to_cart_btn = page.locator(".btn_inventory")
        self.open_cart_button = page.locator(".shopping_cart_link")
        self.checkout_button = page.locator(".checkout_button")
        self.first_name = page.locator("#first-name")
        self.last_name = page.locator("#last-name")
        self.postal_code = page.locator("#postal-code")
        self.continue_button = page.locator("#continue")

        self.inventory_price = page.locator(".inventory_item_price")

        self.subtotal_label = page.locator(".summary_subtotal_label")
        self.total_label = page.locator(".summary_total_label")
        self.tax_label = page.locator(".summary_tax_label")

    def add_to_cart_first_n_products(self, count):
        expected_total = 0.0
        for i in range(count):
            self.add_to_cart_btn.nth(i).click()
            # Витягуємо текст
            price_text = self.inventory_price.nth(i).inner_text()
            price_value = float(price_text.replace("$", ""))
            expected_total += price_value
        return expected_total

    def open_cart(self):
        self.open_cart_button.click()
        return self

    def checkout_start(self):
        self.checkout_button.click()
        return self

    def user_data_fill(self):
        self.first_name.fill("Dohn")
        self.last_name.fill("Joe")
        self.postal_code.fill("10999")
        self.continue_button.click()
        return self

    def get_subtotal(self):
        text = self.subtotal_label.inner_text()
        return float(text.split("$")[1])

    def get_tax_amount(self):
        text = self.tax_label.inner_text()
        return float(text.split("$")[1])

    def get_final_total(self):
        text = self.total_label.inner_text()
        return float(text.split("$")[1])


class NeverPage:
    def __init__(self, page):
        self.page = page
        self.response = None

        # opening the wrong page
    def open_wrong_page(self, url):
        self.response = self.page.goto(f"{url}v1")
        return self.response
