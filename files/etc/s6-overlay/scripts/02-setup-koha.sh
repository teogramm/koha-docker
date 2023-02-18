#!/command/with-contenv bash

export KOHA_INSTANCE=default

export KOHA_INTRANET_PORT=8081
export KOHA_OPAC_PORT=8080
export MEMCACHED_SERVERS=${MEMCACHED_SERVERS:-memcached}
export MYSQL_SERVER=${MYSQL_SERVER:-db}
export DB_NAME=${DB_NAME:-koha_default}
export MYSQL_USER=${DB_NAME:-koha_default}
export MYSQL_PASSWORD=${MYSQL_PASSWORD:-$(pwgen -s 15 1)}
export ZEBRA_MARC_FORMAT=${ZEBRA_MARC_FORMAT:-marc21}
export KOHA_PLACK_NAME=${KOHA_PLACK_NAME:-koha}
export KOHA_ES_NAME=${KOHA_ES_NAME:-es}

# RabbitMQ settings
export MB_HOST=${MB_HOST:-rabbitmq}
export MB_PORT=${MB_PORT:-61613}
export MB_USER=${MB_USER:-guest}
export MB_PASS=${MB_PASS:-guest}

envsubst < /docker/templates/koha-sites.conf > /etc/koha/koha-sites.conf

# Create entry with admin username, password and myqsl server for this instance
echo -n "default:${MYSQL_USER}:${MYSQL_PASSWORD}:${DB_NAME}:${MYSQL_SERVER}" > /etc/koha/passwd

source /usr/share/koha/bin/koha-functions.sh

MB_PARAMS="--mb-host ${MB_HOST} --mb-port ${MB_PORT} --mb-user ${MB_USER} --mb-pass ${MB_PASS}"

# Configure the elasticsearch server
ES_PARAMS=""
if [[ "${USE_ELASTICSEARCH}" = "true" ]]
then
    ES_PARAMS="--elasticsearch-server ${ELASTICSEARCH_HOST}"
fi

if ! is_instance ${KOHA_INSTANCE} || [ ! -f "/etc/koha/sites/${KOHA_INSTANCE}/koha_conf.xml" ]
then
    echo "Executing koha-create for instance ${KOHA_INSTANCE}"
    koha-create ${ES_PARAMS} ${MB_PARAMS} --use-db ${KOHA_INSTANCE} | true
else
    echo "Creating directory structure"
    koha-create-dirs ${KOHA_INSTANCE}
fi

# Configure search daemon
if [ "${USE_ELASTICSEARCH}" = "true" ]
then
    koha-elasticsearch --rebuild -p $(grep -c ^processor /proc/cpuinfo) ${KOHA_INSTANCE} &
fi

for i in $(koha-translate -l)
do
    if [ "${KOHA_LANGS}" = "" ] || ! echo "${KOHA_LANGS}"|grep -q -w $i
    then
        echo "Removing language $i"
        koha-translate -r $i
    else
        echo "Checking language $i"
        koha-translate -c $i
    fi
done

if [ "${KOHA_LANGS}" != "" ]
then
    echo "Installing languages"
    LANGS=$(koha-translate -l)
    for i in $KOHA_LANGS
    do
        if ! echo "${LANGS}"|grep -q -w $i
        then
            echo "Installing language $i"
            koha-translate -i $i
        else
            echo "Language $i already present"
        fi
    done
fi

koha-plack --enable ${KOHA_INSTANCE}
a2enmod proxy

# Prevent Plack from throwing permission errors
touch /var/log/koha/${KOHA_INSTANCE}/opac-error.log /var/log/koha/${KOHA_INSTANCE}/intranet-error.log
chown -R ${KOHA_INSTANCE}-koha:${KOHA_INSTANCE}-koha /var/log/koha/${KOHA_INSTANCE}/

service apache2 stop
koha-indexer --stop ${KOHA_INSTANCE}
koha-zebra --stop ${KOHA_INSTANCE}
koha-worker --stop ${KOHA_INSTANCE}
koha-email-enable ${KOHA_INSTANCE}
