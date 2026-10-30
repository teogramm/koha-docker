import pytest

from koha_docker.test.model.ItemType import Book
from koha_docker.test.model.Library import Springfield
from koha_docker.test.model.Patron import Administrator
from koha_docker.test.model.PatronCategory import Adult
from koha_docker.test.setup.koha_onboarding import KohaOnboarding, OnboardingData
from koha_docker.test.setup.koha_setup import KohaSetup
from koha_docker.test.browser import driver, koha_admin_page, koha_catalog_page, koha_admin_logged_in
from koha_docker.test.setup.container_setup import setup_container, setup_kubernetes_yaml
from koha_docker.test.credentials import database_credentials

@pytest.fixture(scope="session")
def koha_setup(driver, setup_container, database_credentials):
    KohaSetup(driver, database_credentials).run_setup()
    onboarding_data = OnboardingData(Springfield, Adult, Administrator, Book)
    KohaOnboarding(driver).run_onboarding(onboarding_data)