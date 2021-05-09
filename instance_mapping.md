### EC2 Instance Mapping ###


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

ssh -i ./cloudera.pem -N -L 7180:ec2-3-238-247-189.compute-1.amazonaws.com:7180 ubuntu@ec2-3-238-247-189.compute-1.amazonaws.com

https://www.whatsmyip.org


