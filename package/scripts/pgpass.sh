#!/bin/bash
su postgres <<EOF
mkdir /home/postgres;
cd /home/postgres;
touch .pgpass;
echo $1 > .pgpass;

#cd /usr/pgsql-9.5/bin;
#psql -d $2 -c 'create extension pgpool_regclass';
#SSpsql -d $2 -c 'create extension pgpool_recovery';

exit;
EOF
