# tests/test_negative.py
import pytest

def test_not_found(test_never_page):
    assert test_never_page.status == 404
"""
def test_no_img(test_login):
    # There is no valid img for this user
    test_login.login(problem_user, secret_sauce)
    pass
"""
# special user's cases
@pytest.mark.parametrize("username, password, expected_error", [
    pytest.param("standard_user", "wrong_password", "do not match any user", id="wrong_password"),
    pytest.param("locked_out_user", "secret_sauce", "has been locked out", id="locked_out_user"),
    pytest.param("", "secret_sauce", "Username is required", id="empty_username"),
])
def test_login_negative(test_login, username, password, expected_error):
    test_login.login(username, password)
    assert expected_error in test_login.get_error_text()
    assert "inventory.html" not in test_login.page.url

