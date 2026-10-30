import time

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By

from koha_docker.test.model.Patron import Administrator


def click_submit(driver):
    driver.find_element(By.XPATH, '//input[@type="submit"]').click()


OPAC_URL="http://localhost:8080"
ADMIN_URL="http://localhost:8081"


@pytest.fixture(scope="session", autouse=True)
def driver():
    driver = webdriver.Firefox()
    yield driver
    # time.sleep(600)
    # driver.close()


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
def koha_admin_logged_in(driver, koha_admin_page):
    username_input = driver.find_elements(By.ID, "userid")
    if len(username_input) > 0:
        credentials =  Administrator.login
        username_input[0].send_keys(credentials.username)
        password_input = driver.find_element(By.ID, "password")
        password_input.send_keys(credentials.password)
        click_submit(driver)
    yield driver
    driver.find_element(By.ID, "logged-in-menu").click()
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
