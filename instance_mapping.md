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

Cloudera Manager http://localhost:7100 (admin/admin)

ssh -i ./cloudera.pem -N -L 7100:ec2-3-238-246-65.compute-1.amazonaws.com:7100 ubuntu@ec2-3-238-246-65.compute-1.amazonaws.com


