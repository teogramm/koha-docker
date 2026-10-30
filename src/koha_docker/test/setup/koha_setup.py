from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait

from koha_docker.test.browser import click_submit, ADMIN_URL


class KohaSetup:
    """
    Implements the koha setup flow.
    """

    def __init__(self, driver, database_credentials: tuple[str, str]):
        self.driver = driver
        self.database_credentials = database_credentials

    def run_setup(self):
        self.login_page()
        self.select_language()
        self.perl_version()
        self.page_database_info()
        self.marc_version()
        self.default_settings()
        self.setup_complete()

    def login_page(self):
        # TODO: Alternative to driver here, maybe yield to next fixtures?
        self.driver.get(ADMIN_URL)
        self.driver.find_element(By.ID, "userid").send_keys(self.database_credentials[0])
        self.driver.find_element(By.ID, "password").send_keys(self.database_credentials[1])
        self.driver.find_element(By.ID, "submit").click()

    def select_language(self):
        language_select = Select(self.driver.find_element(By.ID, "language"))
        language_select.select_by_value("en")
        click_submit(self.driver)

    def perl_version(self):
        self.driver.find_element(By.XPATH, '//p[contains(text(),"All dependencies installed.")]')
        click_submit(self.driver)

    def page_database_info(self):
        click_submit(self.driver)
        connection_established_text = "Connection established."
        self.driver.find_element(By.XPATH, '//p[text()="{}"]'.format(connection_established_text))
        click_submit(self.driver)
        click_submit(self.driver)
        wait_timeout_seconds = 60
        WebDriverWait(self.driver, wait_timeout_seconds).until(
            expected_conditions.presence_of_element_located((By.XPATH, '//p[text()="Database tables created"]'))
        )
        click_submit(self.driver)
        click_submit(self.driver)

    def marc_version(self):
        self.driver.find_element(By.XPATH, '//input[@id="marcflavour"][@value="MARC21"]')
        click_submit(self.driver)

    def default_settings(self):
        click_submit(self.driver)
        wait_timeout_seconds = 60
        installation_complete_text = "Basic installation complete."
        WebDriverWait(self.driver, wait_timeout_seconds).until(
            expected_conditions.presence_of_element_located(
                (By.XPATH, '//h3[text()="{}"]'.format(installation_complete_text))
            )
        )

    def setup_complete(self):
        click_submit(self.driver)
        self.driver.find_element(By.CLASS_NAME, "btn").click()