from dataclasses import dataclass
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.webdriver import WebDriver

from koha_docker.test.browser import click_submit
from koha_docker.model.ItemType import ItemType
from koha_docker.model.Library import Library
from koha_docker.model.Patron import Patron
from koha_docker.model.PatronCategory import PatronCategory


@dataclass
class OnboardingData:
    library: Library
    patreon_category: PatronCategory
    administrator: Patron
    item_type: ItemType

class KohaOnboarding:
    """
    Implements the Koha Onboarding flow
    """
    
    def __init__(self, driver: WebDriver):
        """
        :param driver: Database driver
        """
        self.driver = driver
        
    def run_onboarding(self, data: OnboardingData):
        self.create_library(data.library)
        self.create_patron_category(data.patreon_category)
        self.create_administrator(data.administrator)
        self.create_item_type(data.item_type)
        self.create_circulation_rule()
        self.driver.find_element(By.CLASS_NAME, "btn-success").click()
        
    def create_library(self, library: Library):
        self.driver.find_element(By.XPATH, '//input[@id="branchcode"]').send_keys(library.code)
        self.driver.find_element(By.XPATH, '//input[@id="branchname"]').send_keys(library.name)
        click_submit(self.driver)
        
    def create_patron_category(self, patron_category: PatronCategory):
        self.driver.find_element(By.XPATH, '//input[@id="categorycode"]').send_keys(patron_category.code)
        self.driver.find_element(By.XPATH, '//input[@id="description"]').send_keys(patron_category.description)
        enrollment_months = str(patron_category.enrollment_months)
        self.driver.find_element(By.XPATH, '//input[@id="enrolmentperiod"]').send_keys(enrollment_months)
        click_submit(self.driver)
        
    def create_administrator(self, administrator: Patron):
        self.driver.find_element(By.XPATH, '//input[@id="surname"]').send_keys(administrator.surname)
        self.driver.find_element(By.XPATH, '//input[@id="firstname"]').send_keys(administrator.first_name)
        self.driver.find_element(By.XPATH, '//input[@id="cardnumber"]').send_keys(administrator.card_number)
        self.driver.find_element(By.XPATH, '//input[@id="userid"]').send_keys(administrator.login.username)
        self.driver.find_element(By.XPATH, '//input[@id="password"]').send_keys(administrator.login.password)
        self.driver.find_element(By.XPATH, '//input[@id="password2"]').send_keys(administrator.login.password)
        click_submit(self.driver)
        
    def create_item_type(self, item_type: ItemType):
        self.driver.find_element(By.XPATH, '//input[@id="itemtype"]').send_keys(item_type.code)
        self.driver.find_element(By.XPATH, '//input[@id="description"]').send_keys(item_type.description)
        click_submit(self.driver)
        
    def create_circulation_rule(self):
        click_submit(self.driver)