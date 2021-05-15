### EC2 Instance Mapping ###

ec2-3-238-247-189.compute-1.amazonaws.com   ip-172-31-89-98.ec2.internal
ec2-44-192-91-57.compute-1.amazonaws.com    ip-172-31-86-76.ec2.internal
ec2-3-236-212-114.compute-1.amazonaws.com   ip-172-31-89-114.ec2.internal
ec2-3-236-144-131.compute-1.amazonaws.com   ip-172-31-84-154.ec2.internal
ec2-3-226-72-155.compute-1.amazonaws.com    ip-172-31-82-207.ec2.internal
ec2-3-236-16-30.compute-1.amazonaws.com     ip-172-31-91-111.ec2.internal


### Access Example ###

kentontroy@DESKTOP-9E2JM4U:~$ chmod 600 cloudera.pem
kentontroy@DESKTOP-9E2JM4U:~$ ssh -i ./cloudera.pem ubuntu@ec2-3-238-246-65.compute-1.amazonaws.com

ubuntu@ip-172-31-89-98:~$ uname -a
Linux ip-172-31-89-98 5.4.0-1045-aws #47~18.04.1-Ubuntu SMP Tue Apr 13 15:58:14 UTC 2021 x86_64 x86_64 x86_64 GNU/Linux

ubuntu@ip-172-31-89-98:~$ mkdir downloads
ubuntu@ip-172-31-89-98:~$ cd downloads
ubuntu@ip-172-31-89-98:~/downloads$ wget https://archive.cloudera.com/cm7/7.1.4/cloudera-manager-installer.bin
ubuntu@ip-172-31-89-98:~/downloads$ chmod u+x cloudera-manager-installer.bin
ubuntu@ip-172-31-89-98:~/downloads$ sudo ./cloudera-manager-installer.bin

Cloudera Manager http://localhost:7180 (admin/admin)

ubuntu@ip-172-31-89-98:~$ sudo iptables -F
ubuntu@ip-172-31-89-98:~/downloads$ sudo vi /etc/ssh/sshd_config
PermitTunnel yes

ubuntu@ip-172-31-89-98:~/downloads$ sudo service sshd restart

ubuntu@ip-172-31-89-98:~/downloads$ sudo lsof -i -P -n | grep LISTEN
systemd-r  727 systemd-resolve   13u  IPv4  18739      0t0  TCP 127.0.0.53:53 (LISTEN)
sshd      1164            root    3u  IPv4  20890      0t0  TCP *:22 (LISTEN)
sshd      1164            root    4u  IPv6  20892      0t0  TCP *:22 (LISTEN)
postgres  4755        postgres    7u  IPv4  32899      0t0  TCP 127.0.0.1:5432 (LISTEN)
postgres  6107    cloudera-scm    3u  IPv4  35104      0t0  TCP *:7432 (LISTEN)
postgres  6107    cloudera-scm    4u  IPv6  35105      0t0  TCP *:7432 (LISTEN)
java      6133    cloudera-scm  470u  IPv4  34358      0t0  TCP *:7182 (LISTEN)
java      6133    cloudera-scm  475u  IPv4  38341      0t0  TCP *:7180 (LISTEN)

Cloudera Manager
ssh -i ./cloudera.pem -N -L 7180:ec2-3-238-247-189.compute-1.amazonaws.com:7180 ubuntu@ec2-3-238-247-189.compute-1.amazonaws.com

Streaming Message Manager
ssh -i ./cloudera.pem -N -L 9991:ec2-3-236-211-223.compute-1.amazonaws.com:9991 ubuntu@ec2-3-236-211-223.compute-1.amazonaws.com

At the instance level, change the Kafka configuration for advertised.host.name to be set to a publicly resolvable name (not IP)

Create an advanced configuration snippet (i.e. a safety valve) containing:

listeners=PLAINTEXT://0.0.0.0:9092,SSL://0.0.0.0:9093

kdavis-MBP15:src kdavis$ export CONFLUENT_HOME=${HOME}/Documents/Confluent_Server/CPE/confluent-5.3.0
kdavis-MBP15:src kdavis$ export PATH=$CONFLUENT_HOME/bin:$PATH

https://www.whatsmyip.org

kentontroy@DESKTOP-9E2JM4U:~$ ssh -i ./cloudera.pem ubuntu@ec2-3-215-182-22.compute-1.amazonaws.com
ubuntu@ip-172-31-90-124:~$ df -m
Filesystem     1M-blocks  Used Available Use% Mounted on
udev                7900     0      7900   0% /dev
tmpfs               1583     2      1582   1% /run
/dev/nvme0n1p1     29716 25563      4137  87% /

In Cloudera Manager, go to Hosts tab.
1. Stop the Roles on the host
2. Remove the Host from the cluster
3. Resize the file system
4. 

df -hT

ubuntu@ip-172-31-90-124:~$ sudo growpart /dev/nvme0n1 1
CHANGED: partition=1 start=2048 old: size=62912479 end=62914527 new: size=125827039,end=125829087

ubuntu@ip-172-31-90-124:~$ sudo resize2fs /dev/nvme1n1


Must have a quorum of at least three Journal Nodes. The Active Name Node writes all edits to a Journal Node and only issues a commit when
all the edits have been replicated to other Journal Nodes. The Standby Name Node uses the Journal Node edits to keep in sync with the Active 
Name Node.

Zookeeper assists with cluster coordination and distributed configuration management. It can be used for leader election should an node runnnig
an active service dies and another node wants to be promoted (e.g. Name Nodes, Kafka broker hosting the leader partition for a Kafka topic, etc.)
ZKFailoverControllers can be used to maintain a lock on a Zookeeper zknode to identify which cluster node is the leader for a service. When that 
lock disappears, other cluster nodes can contend to acquire the lock and be designated the leader.

Use of Active / Standby Name Nodes requires a Name Service to be configured

A Failover Controller should exist on each Name Node instance

A Hive Gateway must exist on the Spark node so that Spark can read from Hive. The Gateway is used to propagate the Hive client configuration to cluster nodes

To start the Spark History server:

ubuntu@ip-172-31-90-124:~$ sudo -u hdfs hadoop fs -ls /user/spark/applicationHistory
ls: `/user/spark/applicationHistory': No such file or directory
ubuntu@ip-172-31-90-124:~$ sudo -u hdfs hadoop fs -mkdir /user/spark/applicationHistory
ubuntu@ip-172-31-90-124:~$ sudo -u hdfs hadoop fs -ls hdfs://demo-nameservice/user/spark/
Found 1 items
drwxr-xr-x   - hdfs supergroup          0 2021-05-10 01:54 hdfs://demo-nameservice/user/spark/applicationHistory

The Cloudera Manager Home page displays a listing of services and their status. Select the menu option next to each service to Start, Stop, and see more detail
on the Instances. The Instances page enables you to see the one-to-many Roles for each Service. Each Cluster Node assuming one or more of those Roles.

kdavis-MBP15:Cloudera kdavis$ ssh -i ./cloudera.pem ubuntu@ec2-3-238-247-189.compute-1.amazonaws.com

http://nifi.apache.org/docs.html

ubuntu@ip-172-31-89-98:/opt/nifi-1.13.2$ sudo apt update
ubuntu@ip-172-31-89-98:/opt/nifi-1.13.2$ sudo apt install default-jdk
ubuntu@ip-172-31-89-98:/opt/nifi-1.13.2$ java -version
openjdk version "11.0.11" 2021-04-20



ubuntu@ip-172-31-89-98:~$ cd downloads
ubuntu@ip-172-31-89-98:~/downloads$ wget https://apache.claz.org/nifi/1.13.2/nifi-1.13.2-bin.tar.gz
ubuntu@ip-172-31-89-98:~/downloads$ wget https://apache.claz.org/nifi/1.13.2/nifi-toolkit-1.13.2-bin.tar.gz
ubuntu@ip-172-31-89-98:~/downloads$ gunzip *
ubuntu@ip-172-31-89-98:~/downloads$ tar xvf nifi-1.13.2-bin.tar
ubuntu@ip-172-31-89-98:~/downloads$ sudo mv nifi-1.13.2 /opt
ubuntu@ip-172-31-89-98:~$ cd /opt/nifi-1.13.2
ubuntu@ip-172-31-89-98:/opt/nifi-1.13.2$ sudo ./bin/nifi.sh install dataflow

ubuntu@ip-172-31-89-98:/opt/nifi-1.13.2$ sudo vi /root/.bashrc
# Demo settings
export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64

ubuntu@ip-172-31-89-98:/opt/nifi-1.13.2$ sudo groupadd nifi
ubuntu@ip-172-31-89-98:/opt/nifi-1.13.2$ sudo usermod -a -G nifi ubuntu
ubuntu@ip-172-31-89-98:/opt/nifi-1.13.2$ sudo chmod -R 775 /opt/nifi-1.13.2
ubuntu@ip-172-31-89-98:/opt/nifi-1.13.2$ sudo chown -R root:nifi /opt/nifi-1.13.2

# Kafka installation

ubuntu@ip-172-31-84-154:~$ ./zookeeper-client
[zk: localhost:2181(CONNECTED) 3] ls /
[confstore, hadoop-ha, hbase, hiveserver2, hiveserver2-leader, kafka, rmstore, solr-infra, yarn-leader-election, zookeeper]
[zk: localhost:2181(CONNECTED) 4] ls /kafka
[admin, brokers, cluster, config, consumers, controller_epoch, delegation_token, isr_change_notification, latest_producer_id_block, log_dir_event_notification]

[zk: localhost:2181(CONNECTED) 7] delete /kafka/cluster/id
[zk: localhost:2181(CONNECTED) 14] sync /kafka/cluster
[zk: localhost:2181(CONNECTED) 15] Sync returned 0

ubuntu@ip-172-31-84-154:~$ sudo find / -name meta.properties
/var/local/kafka/data/meta.properties

ubuntu@ip-172-31-84-154:~$ cat /var/local/kafka/data/meta.properties
#
#Mon May 10 12:43:14 UTC 2021
cluster.id=qy6uhwp3StqgcaiJBlkYrg
version=0
broker.id=1546335377

ubuntu@ip-172-31-84-154:~$ sudo rm /var/local/kafka/data/meta.properties
ubuntu@ip-172-31-86-76:~$ sudo rm /var/local/kafka/data/meta.properties

ubuntu@ip-172-31-89-98:/opt/nifi-1.13.2$ ./bin/nifi.sh start

Installing Nifi in a Cluster managed Zookeeper (Zero-Leader Cluster Paradigm)
https://www.itpanther.com/installing-apache-nifi-cluster-on-linux/

# Install Magenta and TensorFlow dependencies
ubuntu@ip-172-31-89-98:~$ sudo apt-get update -qq && sudo apt-get install -qq libfluidsynth1 fluid-soundfont-gm build-essential libasound2-dev libjack-dev
ubuntu@ip-172-31-89-98:~$ sudo apt install python3-pip
ubuntu@ip-172-31-89-98:~$ pip3 install --upgrade pip
ubuntu@ip-172-31-89-98:~$ pip3 install -qU pyfluidsynth pretty_midi
ubuntu@ip-172-31-89-98:~$ pip3 install -qU tensorflow
ubuntu@ip-172-31-89-98:~$ pip3 install -qU tensorflow-addons
ubuntu@ip-172-31-89-98:~$ pip3 install --ignore-installed -qU magenta




























