#coding=utf-8
import sys, os, pwd, grp, signal, time,logging
from time import sleep
import resource_management
from subprocess import call
from resource_management import *

class PostgreSqlMaster(Script):
    postgresql_package=['postgresql95-server','postgresql95-contrib']
    def install(self,env):
        LANG = 'zh_CN.UTF8'
        #delete PostgreSQL-server
        Execute('service  postgresql-9.5 stop', ignore_failures=True)
        Execute('rpm -e postgresql95-server', ignore_failures=True)
        Execute('rpm -e postgresql95-contrib', ignore_failures=True)
        Execute('rpm -e pgdg-redhat95-9.5-2.noarch', ignore_failures=True)
        #Execute('rm -rf /usr/pgsql-9.5', ignore_failures=True)
        Execute('rm -rf /var/lib/pgsql/9.5', ignore_failures=True)

        import params
        #install new PostgreSql datasource
        psql_datasouse = params.psql_dowload
        print "is psql_datasouse----->" + psql_datasouse
        psql = format('yes | yum install {psql_datasouse}')
        print "is code----->"+psql
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
        #init_db = format("su postgres -c 'initdb -D {psql_data_dir}  --locale={LANG}' ")
        init_db = format("su postgres -c '/usr/pgsql-9.5/bin/initdb -D {psql_data_dir}  --locale={LANG}'")
        Execute(init_db, ignore_failures=True)

        sleep(10)
        #
        self.configure(env)

        sleep(5)
       #start sql
        psql_serverName = params.psql_serverName
        start = format('service {psql_serverName} start ')
        print "启动psql:------>"+start
        Execute(start, ignore_failures=True)

        sleep(10)
        #Set up the database user password
        pwd = params.db_password
        check_user = params.check_user
        service_packagedir = params.service_packagedir
        init_lib_path = service_packagedir + '/scripts/dbpwd.sh'
        File(init_lib_path,
             content=Template("dbpwd.sh.j2"),
             mode=0777
             )
        cmd = format("{service_packagedir}/scripts/dbpwd.sh {pwd} {check_user} ")
        Execute(format("chmod -R 777 {init_lib_path}"), ignore_failures=True)
        Execute('echo "Running ' + cmd + '" as root')
        Execute(cmd)

        ################################
        #install pgpool
        ################################


    def configure(self,env):
        import params
        psql_data_dir = params.psql_data_dir
        #Replace the configuration file
        psql_content = InlineTemplate(params.psql_content)
        File(format('{psql_data_dir}/postgresql.conf'), content=psql_content, owner='postgres')

        psql_pg_hba_content = InlineTemplate(params.psql_pg_hba_content)
        File(format('{psql_data_dir}/pg_hba.conf'), content=psql_pg_hba_content, owner='postgres')




    def start(self,env):
        import params
        psql_serverName = params.psql_serverName
        Execute(format('service {psql_serverName} start '), ignore_failures=True)

    def stop(self,env):
        import params
        psql_serverName = params.psql_serverName
        Execute(format('service  {psql_serverName} stop'), ignore_failures=True)

    def restart(self, env):
        self.configure(env)
        import params
        psql_serverName = params.psql_serverName
        Execute(format(' service  {psql_serverName} restart '), ignore_failures=True)

    def status(self,env):
        Execute("service  postgresql-9.5 status")



if __name__ == "__main__":
    PostgreSqlMaster().execute()