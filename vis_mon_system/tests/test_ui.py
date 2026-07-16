# tests/test_ui.py

def test_count(test_manager):
	actual_count = test_manager.get_prod_count()
	assert actual_count == 6

def test_assert_header(test_manager):
	header_title = test_manager.get_header_text()
	assert header_title == "Products"

def test_assert_card_sum(test_cart):
	total_items_costs = test_cart.add_to_cart_first_n_products(2)

	test_cart.open_cart().checkout_start().user_data_fill()

	assert test_cart.get_final_total() > 0, "Final total cost is equal to zero!!!"
	assert test_cart.get_subtotal() == total_items_costs, "Final total cost is not equal to sum of inventory prices."
	assert round(test_cart.get_final_total(),2) == round(test_cart.get_subtotal() + test_cart.get_tax_amount(),2), "Calculating of tax is wrong."