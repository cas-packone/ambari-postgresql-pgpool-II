#coding=utf-8
from resource_management import *
from resource_management.libraries.script.script import Script
import sys, os, glob,socket
from resource_management.libraries.functions.version import format_hdp_stack_version
from resource_management.libraries.functions.default import default

# server configurations
config = Script.get_config()

service_packagedir = os.path.realpath(__file__).split('/scripts')[0]

#####################################
#PostgreSql config
#####################################
psql_data_dir =  config['configurations']['postgresql']['psql.data.dir']
db_password = config['configurations']['postgresql']['db_password']
psql_model = config['configurations']['postgresql']['psql.model']
check_user = config['configurations']['postgresql']['check_user']
psql_content = config['configurations']['postgresql']['content']

psql_dowload = config['configurations']['postgresql']['psql.dowload.path']
pool_dowload = config['configurations']['postgresql']['pool.dowload.path']
psql_serverName = config['configurations']['postgresql']['psql.serverName']
master_host = config['configurations']['postgresql']['master_host']
psql_port = config['configurations']['postgresql']['psql_port']
default_database = config['configurations']['postgresql']['default_database']

psql_pg_hba_content = config['configurations']['psql-pg-hba']['content']

psql_recovery = config['configurations']['psql-recovery']['content']


##################################
#pgpool-II config
##################################
pool_content = config['configurations']['pgpool']['content']
pool_hba_content = config['configurations']['pool-hba']['content']
pool_pcp_content = config['configurations']['pgpool-pcp']['content']
pool_pid = "/var/run/pgpool/pgpool.pid"

###################################
#postgres .pgpass file
###################################
psql_pgpass = format("{master_host}:{psql_port}:postgres:{check_user}:{check_user}")

###################################
#psql-failover-stream.xml
###################################
failover_stream = config['configurations']['psql-failover-stream']['content']





