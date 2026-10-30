"""
Functions that help run parts of the test suite during local koha development for manual testing or test case
development
"""
import tempfile
from pathlib import Path

from selenium import webdriver

from koha_docker.model.Credentials import Credentials
from koha_docker.model.ItemType import Book
from koha_docker.model.Library import Springfield
from koha_docker.model.Patron import Administrator
from koha_docker.model.PatronCategory import Adult
from koha_docker.test.setup.container_setup import do_setup_container
from koha_docker.test.setup.koha_onboarding import OnboardingData, KohaOnboarding
from koha_docker.test.setup.koha_setup import KohaSetup


def run_and_set_up() -> None:
    """
    Creates a fully configured and onboarded Koha instance.
    """
    credentials = Credentials("example", "example")
    container = do_setup_container(credentials)
    print("Creating Koha instance")
    driver = webdriver.Firefox()
    KohaSetup(driver, credentials).run_setup()
    onboarding_data = OnboardingData(Springfield, Adult, Administrator, Book)
    KohaOnboarding(driver).run_onboarding(onboarding_data)
    driver.close()
    input("Press enter to delete the container...")
    container.delete()


if __name__ == "__main__":
    run_and_set_up()
