import shutil
import subprocess
import tempfile
import time
import requests
from pathlib import Path
from typing import Generator

import pytest

from koha_docker.test.browser import ADMIN_URL
from koha_docker.test.credentials import database_credentials


def _populate_sample_yaml(file_content: str, credentials: tuple[str,str]) -> str:
    """
    Populates the variables in the sample YAML file
    :param file_content: Kubernetes YAML as string
    :param credentials: Tuple with username and password
    :return: Content of the file with variables substituted
    """
    replacements = {
        "%MARIADB_USER%": credentials[0],
        "%MARIADB_PASSWORD%": credentials[1],
        "%MARIADB_ROOT_PASSWORD%": credentials[1]
    }
    for key, value in replacements.items():
        file_content = file_content.replace(key, value)
    return file_content

@pytest.fixture(scope="session")
def setup_kubernetes_yaml(database_credentials) -> Generator[Path,None,None]:
    example_yaml_location = Path(__file__).parent.parent.parent.parent.parent / "examples" / "koha.yaml"
    assert example_yaml_location.exists()
    rabbitmq_plugins = example_yaml_location.parent / "rabbitmq_plugins"
    assert rabbitmq_plugins.exists()
    temp_dir = tempfile.TemporaryDirectory(prefix="koha-test")
    new_yaml_path = Path(temp_dir.name) / "koha.yaml"
    with open(example_yaml_location, "r") as example_file:
        sample_yaml = example_file.read()
        populated_yaml = _populate_sample_yaml(sample_yaml, database_credentials)
        with open(new_yaml_path, "w") as new_yaml_file:
            new_yaml_file.write(populated_yaml)
            new_yaml_file.flush()
    shutil.copy(rabbitmq_plugins, temp_dir.name)
    print("Database credentials: ", database_credentials[0], database_credentials[1])
    yield new_yaml_path
    temp_dir.cleanup()
    
def wait_for_pod_to_initialize():
    max_tries = 15
    time_per_try = 2
    started = False
    n_tries = 0
    while not started and  n_tries < max_tries:
        try:
            if requests.get(ADMIN_URL).status_code == 200:
                started = True
        except requests.exceptions.ConnectionError:
            pass
        if not started:
            n_tries += 1
            time.sleep(time_per_try)
    assert started
        
@pytest.fixture(scope="session")
def setup_container(setup_kubernetes_yaml: Path, request: pytest.FixtureRequest) -> Generator[None, None, None]:
    def delete_pod():
        subprocess.run(["podman", "kube", "down", "--force", setup_kubernetes_yaml.absolute().as_posix()])
    
    podman_run = subprocess.run(["podman", "kube", "play", setup_kubernetes_yaml.absolute().as_posix()],
                                cwd=setup_kubernetes_yaml.parent)
    assert podman_run.returncode == 0, "podman kube play did not exist successfully. Is the pod already running?"
    request.addfinalizer(delete_pod)
    wait_for_pod_to_initialize()
    yield
