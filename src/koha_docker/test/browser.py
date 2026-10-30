import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By

from koha_docker.model.Patron import Administrator

OPAC_URL = "http://localhost:8080"
ADMIN_URL = "http://localhost:8081"


def click_submit(driver):
    driver.find_element(By.XPATH, '//input[@type="submit"]').click()


@pytest.fixture(scope="session", autouse=True)
def driver():
    driver = webdriver.Firefox()
    yield driver
    driver.close()


@pytest.fixture(scope="class")
def koha_admin_page(driver, koha_setup):
    """
    Koha administration page.
    :param driver: WebDriver fixture provided by Selenium.
    :param koha_setup: Koha setup fixture. Represents a fully set up koha instance
    :return: Webdriver with the administration page loaded
    """
    driver.get(ADMIN_URL)
    yield driver


@pytest.fixture(scope="class")
def koha_admin_logged_in(koha_admin_page):
    """
    Provides a driver pointing to a logged-in Koha administration screen. The fixture
    logs out automatically after it is used.
    :param koha_admin_page: Selenium driver pointing to the Koha administration page.
    """
    driver = koha_admin_page
    username_input = driver.find_elements(By.ID, "userid")
    if len(username_input) > 0:
        credentials = Administrator.login
        username_input[0].send_keys(credentials.username)
        password_input = driver.find_element(By.ID, "password")
        password_input.send_keys(credentials.password)
        click_submit(driver)
    yield driver
    logged_in_menu = driver.find_elements(By.ID, "logged-in-menu")
    if len(logged_in_menu) > 0:
        logged_in_menu[0].click()
        driver.find_element(By.ID, "logout").click()
        driver.find_element(By.ID, "userid")


@pytest.fixture(scope="class")
def koha_catalog_page(driver, koha_setup):
    """
    
    :param driver: WebDriver fixture provided by Selenium.
    :param koha_setup: Koha setup fixture. Represents a fully set up koha instance
    :return: Webdriver with the OPAC catalogue page loaded
    """
    driver.get(OPAC_URL)
    yield driver
