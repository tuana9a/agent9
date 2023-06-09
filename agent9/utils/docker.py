"""
Origin code from OpenStack https://opendev.org/openstack/trove
"""

import docker
import logging
import traceback

from typing import Any, Optional
from agent9.configs import cfg


class DockerUtils():
    __docker_client: docker.DockerClient

    def __init__(self, docker_client: docker.DockerClient = docker.from_env()):
        self.__docker_client = docker_client
        pass

    @property
    def client(self):
        return self.__docker_client

    def login(self, container_registry, username, password, **kwargs):
        self.client.login(username, password, registry=container_registry)

    def list_containers(self, **kwargs):
        return self.client.containers.list(**kwargs)

    def stop_container(self,
                       name: str,
                       timeout=cfg.stop_container_timeout_in_seconds,
                       **kwargs):
        container: Any = self.client.containers.get(name)
        container.stop(timeout=timeout)

    def start_container(self, name: str, **kwargs):
        """Start a docker container.

        :param image: docker image.
        :param name: container name.
        :param restart_policy: restart policy.
        :param volumes: e.g.
            {"/host/trove": {"bind": "/container/trove", "mode": "rw"}}
        :param ports: ports is ignored when network_mode="host". e.g.
            {"3306/tcp": 3306}
        :param user: e.g. "1000.1001"
        :param network_mode: One of bridge, none, host
        :param environment: Environment variables
        :param command:
        :return:
        """
        container: Any = None
        try:
            container = self.client.containers.get(name)
            container.start()
        except Exception as e:
            logging.error(traceback.format_exc())

        return container

    def run_container(self,
                      image: str,
                      name: Optional[str],
                      network="bridge",
                      network_mode: Optional[str] = "bridge",
                      user="",
                      volumes={},
                      environment={},
                      command="",
                      detach=True,
                      remove=False,
                      **kwargs):
        """Run command in a container and return the string output list.

        :param image: docker image.
        :param name: container name.
        :param volumes: e.g.
            {"/host/trove": {"bind": "/container/trove", "mode": "rw"}}
        :param user: e.g. "1000.1001"
        :param network_mode: One of bridge, none, host
        :param environment: Environment variables
        :param command:
        :return:
        """

        container: Any = None

        # network param is incompatible with network_mode
        if network:
            container = self.client.containers.run(
                image,
                name=name,
                volumes=volumes,
                environment=environment,
                network=network,
                user=user,
                command=command,
                detach=detach,
            )
        else:
            container = self.client.containers.run(
                image,
                name=name,
                volumes=volumes,
                environment=environment,
                network_mode=network_mode,
                user=user,
                command=command,
                detach=detach,
            )

        # need reload to get container info if detach=True
        # more details see https://docker-py.readthedocs.io/en/stable/containers.html#container-objects
        container.reload()

        return container

    def restart_container(self,
                          name,
                          timeout=cfg.stop_container_timeout_in_seconds,
                          **kwargs):
        container: Any = self.client.containers.get(name)
        container.restart(timeout=timeout)

    def remove_container(self, name, **kwargs):
        try:
            container: Any = self.client.containers.get(name)
            container.remove(force=True)
        except docker.errors.NotFound:  # type: ignore
            pass

    def prune_images(self, **kwargs):
        """Remove unused images."""
        self.client.images.prune(filters={"dangling": False})

    def create_network(self, name, driver="bridge", opts=None, **kwargs):
        return self.client.networks.create(name, driver, opts)

    def inspect_container(self, name, **kwargs):
        container: Any = self.client.containers.get(name)
        return container.attrs

    def get_container_ip(self, name, index=0, network=None, **kwargs):
        container: Any = self.client.containers.get(name)
        network_settings = container.attrs["NetworkSettings"]["Networks"]

        if network:
            return network_settings[network]["IPAddress"]

        which_network = list(network_settings.keys())[index]

        return network_settings[which_network]["IPAddress"]
