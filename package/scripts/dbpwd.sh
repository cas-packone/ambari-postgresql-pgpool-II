#!/bin/bash
su  postgres <<EOF
cd /usr/pgsql-9.5/bin;
psql -c "ALTER USER postgres WITH PASSWORD '"+"$1'"
psql -c "CREATE ROLE $2 login replication encrypted password '"+"$2'"
createuser -p 5432 -s -w pgpool;
createdb -p 5432 -w pgpool pgpool;
psql -d pgpool -c "create extension dblink";
exit;
EOF
