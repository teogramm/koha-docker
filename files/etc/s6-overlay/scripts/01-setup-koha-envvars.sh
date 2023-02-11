#!/command/with-contenv sh
mkdir -p /etc/koha-envvars
echo -n "/usr/share/koha/lib" > /etc/koha-envvars/PERL5LIB
echo -n "/etc/koha/sites/${KOHA_INSTANCE}/koha-conf.xml" > /etc/koha-envvars/KOHA_CONF
echo -n "/usr/share/koha" > /etc/koha-envvars/KOHA_HOME
echo -n "${KOHA_INSTANCE}" > /etc/koha-envvars/INSTANCE_NAME
