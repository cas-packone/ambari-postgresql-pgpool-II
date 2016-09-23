#coding=utf-8
import sys, os, pwd, grp, signal, time
from time import sleep
import resource_management
from subprocess import call
from resource_management import *

class PostgreSqlPool(Script):
    def install(self,env):
        Execute(':pgpool -m fast stop', ignore_failures=True)
        Execute('rpm -e pgpool-II-pg95-3.5.3-1pgdg.rhel6.x86_64', ignore_failures=True)
        import params
        #install pgpool
        pool_dowload = params.pool_dowload
        cmd = format("yes | yum install {pool_dowload}")
        Execute(cmd, ignore_failures=True)
        sleep(10)

        #set up pool config
        self.configure(env)

        sleep(5)

        #start pool
        cmd_run = 'pgpool -n &'
        Execute(cmd_run, ignore_failures=True)


    def configure(self,env):
        import params
        pool_path = '/etc/pgpool-II'
        pool_hba = InlineTemplate(params.pool_hba_content)
        File(format('{pool_path}/pool_hba.conf'), content=pool_hba, owner='root')

        pool_pcp = InlineTemplate(params.pool_pcp_content)
        File(format('{pool_path}/pcp.conf'), content=pool_pcp, owner='root')

        pool = InlineTemplate(params.pool_content)
        File(format('{pool_path}/pgpool.conf'), content=pool, owner='root')

        Execute('mkdir /var/log/pgpool', ignore_failures=True)

        #failover 生成
        failover_stream = InlineTemplate(params.failover_stream)
        if os.path.exists("/home/postgres/scripts"):
            if not os.path.isfile("/home/postgres/scripts/failover_stream.sh"):
                Execute('touch /home/postgres/scripts/failover_stream.sh', ignore_failures=True)
                File(format('/home/postgres/scripts/failover_stream.sh'), content=failover_stream, owner='root')
            else:
                File(format('/home/postgres/scripts/failover_stream.sh'), content=failover_stream, owner='root')
        else:
            os.makedirs("/home/postgres/scripts")
            Execute('touch /home/postgres/scripts/failover_stream.sh', ignore_failures=True)
            File(format('/home/postgres/scripts/failover_stream.sh'), content=failover_stream, owner='root')

        Execute('chmod 755 /home/postgres/scripts/failover_stream.sh', ignore_failures=True)








    def start(self,env):
        print "start pgpoool"
        cmd_run = 'pgpool -n &'
        Execute(cmd_run, ignore_failures=True)


    def stop(self,env):
        cmd_stop = 'pgpool -m fast stop'
        Execute(cmd_stop, ignore_failures=True)

    def restart(self, env):
        print("restart")
        self.configure(env)
        self.stop(env)
        self.start(env)

    def status(self,env):
        Execute("service pgpool status")



if __name__ == "__main__":
    PostgreSqlPool().execute()