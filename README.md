# koha-docker

![Docker Image Version (tag latest semver)](https://img.shields.io/docker/v/teogramm/koha/22.11)

A Koha Docker container which includes:
* The Apache webserver serving the OPAC (Port 8080) and
the Koha staff interface (Port 8081), configured to use Plack.
* The Zebra server and indexer.
* The Koha background jobs worker.

A fully functional Koha instance additionally requires:
* A MySQL/MariaDB server.
* A Memcached server.
* A RabbitMQ server with the stomp pulgin enabled.

Elasticsearch is also supported, instead of Zebra.

*Notice: SIP and Z3950 are still WIP.*

A separate RabbitMQ server with the stomp plugin is required as well as a Memcached server.
Both can be easily created using the images available on Docker Hub.

## Usage
The image is available on [Docker Hub](https://hub.docker.com/r/teogramm/koha)

The main configuration environment variables are documented in
[config-main.env](config-main.env).

For a quick start check out the included [docker-compose](examples/docker-compose.yaml) file.

Logs for stored under the `/var/log/koha` directory.

## Credits

Some scripts have been taken from https://gitlab.com/koha-community/docker/koha-docker and modified.

