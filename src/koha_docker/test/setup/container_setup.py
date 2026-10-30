import re
import shutil
import subprocess
import tempfile
import time
from abc import ABC, abstractmethod
from pathlib import Path

import requests

from koha_docker.model.Credentials import Credentials
from koha_docker.test.browser import ADMIN_URL


class ContainerApplication(ABC):

    @staticmethod
    @abstractmethod
    def create_and_start_container(definition_file: Path) -> None:
        """
        Creates and starts one or more container from the given definition file.
        :param definition_file: Path to the definition file.
        """

    @staticmethod
    @abstractmethod
    def stop_container(definition_file: Path) -> None:
        """
        Stops the container defined by the given definition file.
        :param definition_file: Path to the definition file.
        """
        # TODO: This could be stateful. Extract the name from the file during creation

    @staticmethod
    @abstractmethod
    def delete_container(definition_file: Path) -> None:
        """
        Deletes the container from the given definition file.
        :param definition_file: Path to the definition file.
        """


class PodmanPod(ContainerApplication):

    @staticmethod
    def _extract_pod_name(kubernetes_yaml: str) -> str:
        """
        Extracts the name of the pod, given the Kubernetes YAML file contents.
        :param kubernetes_yaml: Contents of a Kubernetes YAML file
        :return: Name of the pod defined in the file
        """
        name_regex = r".*metadata.*name:\s*([\d\w]+)"
        match = re.search(name_regex, kubernetes_yaml, flags=re.DOTALL)
        if match:
            return match.group(1)
        else:
            raise ValueError("The given YAML file does not contain any ")

    @staticmethod
    def create_and_start_container(definition_file: Path) -> None:
        """
        Creates a Podman pod using the given Kubernetes YAML file.
        :param definition_file: Kubernetes YAML file.
        """
        podman_run = subprocess.run(["podman", "kube", "play", definition_file.absolute().as_posix()],
                                    cwd=definition_file.parent)
        assert podman_run.returncode == 0, "podman kube play did not exist successfully. Is the pod already running?"

    @staticmethod
    def stop_container(definition_file: Path) -> None:
        # TODO: this class can be made stateful to avoid reading the file every single time 
        with open(definition_file, "r") as file:
            pod_name = PodmanPod._extract_pod_name(file.read())
        podman_cmd = subprocess.run(["podman", "pod", "stop", pod_name])
        assert podman_cmd.returncode == 0

    @staticmethod
    def delete_container(definition_file: Path) -> None:
        """
        Deletes the Podman pod specified in the given Kubernetes YAML file. 
        :param definition_file: Kubernetes YAML file
        """
        subprocess.run(["podman", "kube", "down", "--force", definition_file.absolute().as_posix()])


class KohaContainer:
    # TODO: Make this better
    rabbitmq_plugins_file = Path(__file__).parent.parent.parent.parent.parent / "examples" / "rabbitmq_plugins"

    @staticmethod
    def _populate_sample_yaml(file_content: str, credentials: Credentials) -> str:
        """
        Populates the variables in the sample YAML file
        :param file_content: Kubernetes YAML as string
        :param credentials: Tuple with username and password
        :return: Content of the file with variables substituted
        """
        replacements = {
            "%MARIADB_USER%": credentials.username,
            "%MARIADB_PASSWORD%": credentials.password,
            "%MARIADB_ROOT_PASSWORD%": credentials.password
        }
        for key, value in replacements.items():
            file_content = file_content.replace(key, value)
        return file_content

    def _create_container_definition(self, container_definition_template: Path):
        assert container_definition_template.exists()
        assert self.rabbitmq_plugins_file.exists()
        self.definition_file = Path(self._tempdir.name) / "koha.yaml"
        with open(container_definition_template, "r") as example_file:
            sample_yaml = example_file.read()
            populated_yaml = self._populate_sample_yaml(sample_yaml, self._credentials)
            with open(self.definition_file, "w") as new_yaml_file:
                new_yaml_file.write(populated_yaml)
                new_yaml_file.flush()
        shutil.copy(self.rabbitmq_plugins_file, self._tempdir.name)

    def __init__(self, container_application: ContainerApplication, container_definition_template: Path,
                 database_credentials: Credentials) -> None:
        self._tempdir = tempfile.TemporaryDirectory(prefix="koha-docker-")
        self._credentials = database_credentials
        self._container_application = container_application
        self._create_container_definition(container_definition_template)
        print("Database credentials: ", database_credentials.username, database_credentials.password)
        self._container_application.create_and_start_container(self.definition_file)
        wait_for_pod_to_initialize()

    def delete(self):
        subprocess.run(["podman", "kube", "down", "--force", self.definition_file.absolute().as_posix()])

    def __del__(self):
        self._tempdir.cleanup()


def wait_for_pod_to_initialize(timeout_seconds: int = 30) -> None:
    """
    Waits until the pod initialises and is ready to be used. It waits until the koha admin interface is reachable.
    If max_timeout is reached an assertion error is raised.
    :return: None, when the container is initialised.
    """
    time_per_try = 2
    started = False
    n_tries = 0
    while not started and n_tries * time_per_try < timeout_seconds:
        try:
            if requests.get(ADMIN_URL).status_code == 200:
                started = True
        except requests.exceptions.ConnectionError:
            pass
        if not started:
            n_tries += 1
            time.sleep(time_per_try)
    assert started


def do_setup_container(database_credentials: Credentials) -> KohaContainer:
    """
    Sets up a pod from the given Kubernetes YAML file and waits for it to initialise.
    This function simply creates the given container. It's up to the caller to call the cleanup function. 
    :param database_credentials: Username and password for the database connection
    :return: KohaContainer instance
    """
    kubernetes_yaml = Path(__file__).parent.parent.parent.parent.parent / "examples" / "koha.yaml"
    container = KohaContainer(PodmanPod(), kubernetes_yaml, database_credentials)
    return container
