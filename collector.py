from prometheus_client import Gauge, CollectorRegistry, generate_latest
import time
import os, sys
from flask import Flask
import socket

app = Flask(__name__)
host_name = socket.gethostname()
resource_name = "eimmo-batch-vms" # 리소스 그룹 이름
service_name = "eimmo-batch-vms-worker3" # 서비스 이름 (호스트 이름)


def get_machine_cpu():
    import psutil
    cpu = psutil.cpu_percent(interval=1, percpu=True)
    print(f'{cpu}')


@app.route('/about')
def about():
    return "metric_collector for vm\n", 200


@app.route('/metric/cpu')
def view_cpu():
    import psutil
    keys = {"azure_vm_cpu_percent": {"instance": "", "metric": "cpu_percent", "resource": resource_name, "service": service_name}}

    metrics = []

    registry = CollectorRegistry()

    datas = {"azure_vm_cpu_percent": psutil.cpu_percent()}
    for key in keys.keys():
        label = keys[key]
        label["instance"] = host_name
        metric_num = datas[key]
        gauge = Gauge(key, key, label.keys(), registry=registry)
        label_values = label.values()
        gauge.labels(*label_values).set(metric_num)
    metric = generate_latest(registry=registry)
    metrics.append(metric.decode('utf-8'))

    metric_str = "\n".join(metrics)
    return metric_str, 200


@app.route('/metric/disk')
def view_disk():
    import psutil

    keys = {"azure_vm_disk_total":{"instance": "", "device": "", "metric": "disk_total", "resource": resource_name, "service": service_name},
            "azure_vm_disk_used":{"instance": "", "device": "", "metric": "disk_used" , "resource": resource_name, "service": service_name},
            "azure_vm_disk_used_percent":{"instance": "", "device": "", "metric": "disk_used_percent", "resource": resource_name, "service": service_name}}

    metrics = []

    for disk in psutil.disk_partitions():
        if disk.fstype and 'loop' not in disk.device:
            registry = CollectorRegistry()
            total = round(int(psutil.disk_usage(disk.mountpoint).total)/(1024.0**3),4)
            used  = round(int(psutil.disk_usage(disk.mountpoint).used)/(1024.0**3),4)
            free  = round(int(psutil.disk_usage(disk.mountpoint).free)/(1024.0**3),4)
            used_percent = (used / total) * 100

            datas = {"azure_vm_disk_total":total,
                     "azure_vm_disk_used":used,
                     "azure_vm_disk_used_percent":used_percent}
            for key in keys.keys():
                label = keys[key]
                label["instance"] = host_name
                label["device"] = disk.device
                metric_num = datas[key]
                gauge = Gauge(key, key, label.keys(), registry=registry)
                label_values = label.values()
                gauge.labels(*label_values).set(metric_num)
            metric = generate_latest(registry=registry)
            metrics.append(metric.decode('utf-8'))

    metric_str = "\n".join(metrics)
    return metric_str, 200

@app.route('/metric/memory')
def view_memory():
    
    import psutil
    
    keys = {"azure_vm_mem_total":{"instance": "", "metric": "mem_total", "resource": resource_name, "service": service_name},
            "azure_vm_mem_used":{"instance": "", "metric": "mem_used", "resource": resource_name, "service": service_name},
            "azure_vm_mem_used_percent":{"instance": "", "metric": "mem_used_percent", "resource": resource_name, "service": service_name}}
    
    mem = psutil.virtual_memory()
    ##total=950054912, available=117116928, percent=87.7, used=675012608, free=68538368
    #print(f'{mem.total}, {mem.available}, {mem.free}, {mem.used}')

    metrics = []

    registry = CollectorRegistry()
    total = mem.total
    used  = mem.used
    free  = mem.free
    used_percent = (used / total) * 100

    datas = {"azure_vm_mem_total":total,
             "azure_vm_mem_used":used,
             "azure_vm_mem_used_percent":used_percent}

    for key in keys.keys():
        label = keys[key]
        label["instance"] = host_name
        metric_num = datas[key]
        gauge = Gauge(key, key, label.keys(), registry=registry)
        label_values = label.values()
        gauge.labels(*label_values).set(metric_num)
    metric = generate_latest(registry=registry)
    metrics.append(metric.decode('utf-8'))

    metric_str = "\n".join(metrics)
    return metric_str, 200


def main():
    app.run(host="0.0.0.0",port=5001)


def run_as_fork():
    pid = os.fork()
    if pid > 0:
        exit(0)
    else:
        os.chdir("/")
        os.setsid()
        os.umask(0)

        pid = os.fork()
        if pid > 0:
            exit(0)
        else:
            sys.stdin.flush()
            sys.stdout.flush()

            si = open(os.devnull, 'r')
            so = open(os.devnull, 'a+')
            se = open(os.devnull, 'a+')

            os.dup2(si.fileno(), sys.stdin.fileno())
            os.dup2(so.fileno(), sys.stdout.fileno())
            os.dup2(se.fileno(), sys.stderr.fileno())

            with open("/var/run/collector.pid","w") as write:
                write.write(str(os.getpid()))

            main()

        os.umask(0)

        pid = os.fork()
        if pid > 0:
            exit(0)
        else:
            sys.stdin.flush()
            sys.stdout.flush()

            si = open(os.devnull, 'r')
            so = open(os.devnull, 'a+')
            se = open(os.devnull, 'a+')

            os.dup2(si.fileno(), sys.stdin.fileno())
            os.dup2(so.fileno(), sys.stdout.fileno())
            os.dup2(se.fileno(), sys.stderr.fileno())

            with open("/var/run/collector.pid","w") as write:
                write.write(str(os.getpid()))

            main()


def print_usage():
    print("python collector.py [options]")
    print("------------------------------")
    print("options:")
    print("  -d : run as forked daemon")
    print("  -p : run as self process")


if __name__ == '__main__':
    args = sys.argv[1:]
    if len(args) == 0:
        run_as_fork()
    if args[0] == "-d":
        run_as_fork()
    elif args[0] == "-p":
        main()
    else:
        print_usage()
