# prometheus_system_metric_collector

# 실행환경 구성
```
simpson@ububtu :~/bin$ sudo apt install python3.8-venv
Reading package lists... Done
Building dependency tree       
Reading state information... Done
The following NEW packages will be installed:
  python3.8-venv
0 upgraded, 1 newly installed, 0 to remove and 37 not upgraded.
Need to get 5448 B of archives.
After this operation, 27.6 kB of additional disk space will be used.
Get:1 http://azure.archive.ubuntu.com/ubuntu focal-updates/universe amd64 python3.8-venv amd64 3.8.10-0ubuntu1~20.04.6 [5448 B]
Fetched 5448 B in 0s (247 kB/s)    
Selecting previously unselected package python3.8-venv.
(Reading database ... 205927 files and directories currently installed.)
Preparing to unpack .../python3.8-venv_3.8.10-0ubuntu1~20.04.6_amd64.deb ...
Unpacking python3.8-venv (3.8.10-0ubuntu1~20.04.6) ...
Setting up python3.8-venv (3.8.10-0ubuntu1~20.04.6) ...
simpson@ububtu :~/bin$ python -m venv venv
simpson@ububtu :~/bin$ source venv/bin/activate
simpson@ububtu :~/bin$ python -m pip install pip==9.0.3
simpson@ububtu :~/bin$ pip install -r requirements.txt
```

# 서비스 등록
```
simpson@ububtu :~/$sudo mkdir -p /opt/collector
simpson@ububtu :~/$sudo cp ./bin/collector /opt/collector
simpson@ububtu :~/$sudo su - && cd /opt/collector
root@ubuntu :/opt/collector$ apt install python3.8-venv gcc python3-dev
root@ubuntu :/opt/collector$ python -m venv venv
root@ubuntu :/opt/collector$ source venv/bin/activate
root@ubuntu :/opt/collector$ python -m pip install pip==9.0.3
root@ubuntu ::opt/collector$ pip install -r requirements.txt
root@ubuntu :/etc/systemd/system# vi collector.service
root@ubuntu :/etc/systemd/system# systemctl daemon-reload
root      783276  751943  0 13:21 pts/0    00:00:00 grep --color=auto collec
root@ubuntu :/etc/systemd/system# systemctl start collector
root@ubuntu :/etc/systemd/system# systemctl status collector
● collector.service - Collector Service.
     Loaded: loaded (/etc/systemd/system/collector.service; enabled; vendor preset: enabled)
     Active: active (running) since Fri 2023-02-24 13:21:13 KST; 6s ago
    Process: 783284 ExecStart=/bin/bash -c source /opt/collector/venv/bin/activate && python /opt/collector/collector.py (code=exited, status>
   Main PID: 783287 (python)
      Tasks: 1 (limit: 4095)
     Memory: 17.8M
     CGroup: /system.slice/collector.service
             └─783287 python /opt/collector/collector.py

Feb 24 13:21:13 ubuntu systemd[1]: Starting Collector Service....
Feb 24 13:21:13 ubuntu systemd[1]: collector.service: Supervising process 783287 which is not our child. We'll most likely n>
Feb 24 13:21:13 ubuntu systemd[1]: Started Collector Service..
root@ubuntu :/etc/systemd/system# systemctl stop collector:~/$sudo mkdir -p /opt/collector
simpson@ububtu :~/$sudo cp ./bin/collector /opt/collector
simpson@ububtu :~/$sudo su - && cd /opt/collector
root@ubuntu :/opt/collector$ apt install python3.8-venv gcc python3-dev
root@ubuntu :/opt/collector$ python -m venv venv
root@ubuntu :/opt/collector$ source venv/bin/activate
root@ubuntu :/opt/collector$ python -m pip install pip==9.0.3
root@ubuntu ::opt/collector$ pip install -r requirements.txt
root@ubuntu :/etc/systemd/system# vi collector.service
root@ubuntu :/etc/systemd/system# systemctl daemon-reload
root      783276  751943  0 13:21 pts/0    00:00:00 grep --color=auto collec
root@ubuntu :/etc/systemd/system# systemctl start collector
root@ubuntu :/etc/systemd/system# systemctl status collector
● collector.service - Collector Service.
     Loaded: loaded (/etc/systemd/system/collector.service; enabled; vendor preset: enabled)
     Active: active (running) since Fri 2023-02-24 13:21:13 KST; 6s ago
    Process: 783284 ExecStart=/bin/bash -c source /opt/collector/venv/bin/activate && python /opt/collector/collector.py (code=exited, status>
   Main PID: 783287 (python)
      Tasks: 1 (limit: 4095)
     Memory: 17.8M
     CGroup: /system.slice/collector.service
             └─783287 python /opt/collector/collector.py

Feb 24 13:21:13 ubuntu systemd[1]: Starting Collector Service....
Feb 24 13:21:13 ubuntu systemd[1]: collector.service: Supervising process 783287 which is not our child. We'll most likely n>
Feb 24 13:21:13 ubuntu systemd[1]: Started Collector Service..
root@ubuntu :/etc/systemd/system# systemctl stop collector
```
