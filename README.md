# ambari-postgresql-pgpool-II
  install hue on Web Page

#注意:
  如果ambari使用的数据库是自带的PostgreSql的话,postgresql数据库集群中的任何一个节点都不要安装在ambari服务所在的主机上.
  
# 安装主库和pgpool
![Image](../master/screenshots/1.png?raw=true)
![Image](../master/screenshots/2-1.png?raw=true)
![Image](../master/screenshots/2-2.png?raw=true)
![Image](../master/screenshots/2-3.png?raw=true)
![Image](../master/screenshots/3-1.png?raw=true)
![Image](../master/screenshots/3-2.png?raw=true)
![Image](../master/screenshots/4-1.png?raw=true)
![Image](../master/screenshots/5-1.png?raw=true)
![Image](../master/screenshots/5-2.png?raw=true)
![Image](../master/screenshots/5-3.png?raw=true)
![Image](../master/screenshots/6.png?raw=true)
![Image](../master/screenshots/7-1.png?raw=true)
![Image](../master/screenshots/7-2.png?raw=true)
![Image](../master/screenshots/8-1.png?raw=true)
![Image](../master/screenshots/8-2.png?raw=true)
![Image](../master/screenshots/8-3.png?raw=true)

# 安装slave
  在安装master的时候后,pgpool的配置文件中配置了从机(slave)分别是packOne40/packOne41/packOne42.现在我们就对在着三台主机上安装上psql slave.这里以40为例:
![Image](../master/screenshots/9-1.png?raw=true)
![Image](../master/screenshots/9-2.png?raw=true)
![Image](../master/screenshots/9-3.png?raw=true)
![Image](../master/screenshots/9-4.png?raw=true)
![Image](../master/screenshots/9-5.png?raw=true)
![Image](../master/screenshots/9-6.png?raw=true)
![Image](../master/screenshots/9-7.png?raw=true)
  使用同样的方法,将剩下的主机安装上slave.
![Image](../master/screenshots/9-8.png?raw=true)
![Image](../master/screenshots/9-9.png?raw=true)

