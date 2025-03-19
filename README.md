# koha-docker

![Docker Image Version (tag latest semver)](https://img.shields.io/docker/v/teogramm/koha/latest)

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

The username and password for the initial setup are the same as the database username and password.

Logs for stored under the `/var/log/koha` directory.

In order to function, Koha requires a MySQL database, a Memcached server and a RabbitMQ server with the stomp plugin.

The provided [docker-compose file](examples/docker-compose.yaml) sets up all of these as containers. It provides an easy way to
get a Koha insstance up and running. For a production environment it is recommened that each container is set up separately.

## Credits

Some scripts have been taken from https://gitlab.com/koha-community/docker/koha-docker and modified.

