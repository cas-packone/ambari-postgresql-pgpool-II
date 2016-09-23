#coding=utf-8
import sys, os, pwd, grp, signal, time,logging
from time import sleep
import resource_management
from subprocess import call
from resource_management import *

class PostgreSqlSlave(Script):
    postgresql_package = ['postgresql95-server', 'postgresql95-contrib']
    def install(self,env):
        LANG = 'zh_CN.UTF8'
        #delete PostgreSQL-server
        Execute("service  postgresql-9.5 stop", ignore_failures=True)
        Execute('rpm -e postgresql95-server', ignore_failures=True)
        Execute('rpm -e postgresql95-contrib', ignore_failures=True)
        Execute('rpm -e pgdg-redhat95-9.5-2.noarch', ignore_failures=True)
        #Execute('rm -rf /usr/pgsql-9.5', ignore_failures=True)
        Execute('rm -rf /var/lib/pgsql/9.5', ignore_failures=True)
        Execute('chmod -R 777 /home', ignore_failures=True)

        import params
        # install new PostgreSql datasource
        psql_datasouse = params.psql_dowload
        print "is psql_datasouse----->" + psql_datasouse
        psql = format('yes | yum install {psql_datasouse}')
        print "is code----->" + psql
        Execute(psql)
        sleep(15)
        self.install_packages(env)
        print 'install PostgreSql '
        if self.postgresql_package is not None and len(self.postgresql_package):
            for pack in self.postgresql_package:
                Package(pack)
                sleep(10)

        sleep(5)
        #set psql
        #Set the startup
        serverName = params.psql_serverName
        Execute(format('chkconfig {serverName} on '), ignore_failures=True)

        #set datasource permissions
        psql_data_dir = params.psql_data_dir
        Execute(format('chown -R postgres.postgres {psql_data_dir} '), ignore_failures=True)
        Execute(format('chmod -R go-rwx {psql_data_dir} '), ignore_failures=True)

        #init db
        psql_model = params.psql_model
        if psql_model != 'ms':
            Execute(format("su postgres -c '/usr/pgsql-9.5/bin/initdb -D {psql_data_dir}  --locale={LANG}'"), ignore_failures=True)
        else:
            master_host = params.master_host
            psql_port = params.psql_port
            Execute(format('mkdir {psql_data_dir} '), ignore_failures=True)
            Execute(format('su postgres -c "pg_basebackup -D {psql_data_dir} -Fp -Xs -v -P -h {master_host} -U replica -p {psql_port}" '), ignore_failures=True)

        sleep(15)

        #
        self.configure(env)


       #start sql
        Execute(format('service {serverName} start '), ignore_failures=True)

        sleep(5)
        #Set up the database user password when psql_model is not "ms",because "ms" is master/slave,Slave is only allowed to read.so default
        if psql_model != 'ms':
            pwd = params.db_password
            service_packagedir = params.service_packagedir
            init_lib_path = service_packagedir + '/scripts/dbslave.sh'
            File(init_lib_path,
                 content=Template("dbslave.sh.j2"),
                 mode=0777
                 )
            cmd = format("{service_packagedir}/scripts/dbslave.sh {pwd}")
            Execute('echo "Running ' + cmd + '" as root')
            Execute(cmd)

        ################################
        #
        ################################


    def configure(self,env):
        import params
        psql_data_dir = params.psql_data_dir
        # Replace the configuration file
        psql_content = InlineTemplate(params.psql_content)
        File(format('{psql_data_dir}/postgresql.conf'), content=psql_content, owner='postgres')

        psql_pg_hba_content = InlineTemplate(params.psql_pg_hba_content)
        File(format('{psql_data_dir}/pg_hba.conf'), content=psql_pg_hba_content, owner='postgres')



        # If it is copied flow way, so you need to install 'pgpool_regclass pgpool_recovery', and generate 'pgpass' files
        psql_model = params.psql_model
        if psql_model == 'ms':
            psql_pgpass = params.psql_pgpass
            default_database = params.default_database
            service_packagedir = params.service_packagedir
            init_lib_path = service_packagedir + '/scripts/pgpass.sh'
            File(init_lib_path,
                 content=Template("pgpass.sh.j2"),
                 mode=0777
                 )
            cmd = format("{service_packagedir}/scripts/pgpass.sh {psql_pgpass} {default_database}")
            Execute('echo "Running ' + cmd + '" as root')
            Execute(cmd)

            env.set_params(params)
            Execute('cp /usr/pgsql-9.5/share/recovery.conf.sample {psql_data_dir}/recovery.conf ', ignore_failures=True)
            psql_recovery = InlineTemplate(params.psql_recovery)
            File(format('{psql_data_dir}/recovery.conf'), content=psql_recovery, owner='postgres')

        else:
            Execute('rm -f {psql_data_dir}/recovery.conf', ignore_failures=True)






    def start(self,env):
        import params
        serverName = params.psql_serverName
        Execute(format('service {serverName} start '), ignore_failures=True)


    def stop(self,env):
        import params
        serverName = params.psql_serverName
        Execute(format('service {serverName} stop'), ignore_failures=True)

    def restart(self, env):
        import params
        self.configure(env)
        serverName = params.psql_serverName
        Execute(format(' service  {serverName} restart '), ignore_failures=True)

    def status(self,env):
        Execute("service  postgresql-9.5 status")


if __name__ == "__main__":
    PostgreSqlSlave().execute()