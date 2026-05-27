import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from utils.helpers import login, wait_for_inventory

@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    yield driver
    driver.quit()

def test_login_success(driver):
    login(driver, "standard_user", "secret_sauce")
    url = wait_for_inventory(driver)
    assert "/inventory.html" in url
    assert "Swag Labs" in driver.title

def test_inventory_page(driver):
    login(driver, "standard_user", "secret_sauce")
    wait_for_inventory(driver)
    title = driver.find_element(By.CLASS_NAME, "title").text
    assert title == "Products"
    products = driver.find_elements(By.CLASS_NAME, "inventory_item")
    assert len(products) > 0
    first_name = products[0].find_element(By.CLASS_NAME, "inventory_item_name").text
    first_price = products[0].find_element(By.CLASS_NAME, "inventory_item_price").text
    print(f"Primer producto: {first_name} - {first_price}")

def test_add_to_cart(driver):
    login(driver, "standard_user", "secret_sauce")
    wait_for_inventory(driver)
    driver.find_element(By.CLASS_NAME, "btn_inventory").click()
    badge = driver.find_element(By.CLASS_NAME, "shopping_cart_badge").text
    assert badge == "1"
    driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()
    cart_item = driver.find_element(By.CLASS_NAME, "inventory_item_name").text
    assert cart_item != ""
