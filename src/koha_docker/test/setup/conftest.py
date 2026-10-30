import tempfile
from pathlib import Path
from typing import Generator

import pytest

from koha_docker.model.Credentials import Credentials
from koha_docker.model.ItemType import Book
from koha_docker.model.Library import Springfield
from koha_docker.model.Patron import Administrator
from koha_docker.model.PatronCategory import Adult
from koha_docker.test.setup.container_setup import do_setup_container
from koha_docker.test.setup.koha_onboarding import OnboardingData, KohaOnboarding
from koha_docker.test.setup.koha_setup import KohaSetup


@pytest.fixture(scope="session")
def setup_container(database_credentials: Credentials) -> Generator[None, None, None]:
    """
    Provides a container with Koha installed.
    :param database_credentials: Credentials for accessing the database.
    """
    container = do_setup_container(database_credentials)
    yield
    container.delete()


@pytest.fixture(scope="session")
def koha_setup(driver, setup_container, database_credentials):
    """
    Provides a fully set up and onboarded Koha instance. 
    :param driver: Selenium driver
    :param setup_container: The container must be created and running.
    :param database_credentials: Credentials for accessing the database.
    """
    KohaSetup(driver, database_credentials).run_setup()
    # TODO: Tidy up this sample data
    onboarding_data = OnboardingData(Springfield, Adult, Administrator, Book)
    KohaOnboarding(driver).run_onboarding(onboarding_data)
