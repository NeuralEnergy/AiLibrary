"""
```bash
neural@neuralserver05:~$ kubectl get all -A -o=wide
NAMESPACE     NAME                                           READY   STATUS             RESTARTS         AGE     IP             NODE             NOMINATED NODE   READINESS GATES
kube-system   pod/calico-kube-controllers-7ddc4f45bc-khtqx   1/1     Running            94 (67m ago)     3d      172.16.53.93   neuralserver05   <none>           <none>
kube-system   pod/calico-node-2b6qt                          0/1     Running            42 (67m ago)     3d      192.168.1.55   neuralserver05   <none>           <none>
kube-system   pod/calico-node-8gn5s                          0/1     CrashLoopBackOff   31 (4m55s ago)   156m    192.168.1.53   neuralserver03   <none>           <none>
kube-system   pod/calico-node-jh28k                          0/1     CrashLoopBackOff   40 (4m25s ago)   3h25m   192.168.1.51   neuralserver     <none>           <none>
kube-system   pod/calico-node-tgqtj                          0/1     CrashLoopBackOff   31 (2m32s ago)   156m    192.168.1.52   neuralserver02   <none>           <none>
kube-system   pod/calico-node-zgnvn                          0/1     Running            32 (5m6s ago)    156m    192.168.1.54   neuralserver04   <none>           <none>
kube-system   pod/coredns-5dd5756b68-b76b8                   1/1     Running            65 (67m ago)     3d1h    172.16.53.94   neuralserver05   <none>           <none>
kube-system   pod/coredns-5dd5756b68-r8szv                   1/1     Running            66 (67m ago)     3d1h    172.16.53.95   neuralserver05   <none>           <none>
kube-system   pod/etcd-neuralserver05                        1/1     Running            185 (67m ago)    3d1h    192.168.1.55   neuralserver05   <none>           <none>
kube-system   pod/kube-apiserver-neuralserver05              1/1     Running            165 (67m ago)    3d1h    192.168.1.55   neuralserver05   <none>           <none>
kube-system   pod/kube-controller-manager-neuralserver05     1/1     Running            176 (67m ago)    3d1h    192.168.1.55   neuralserver05   <none>           <none>
kube-system   pod/kube-proxy-5gd6q                           1/1     Running            28 (5m17s ago)   156m    192.168.1.54   neuralserver04   <none>           <none>
kube-system   pod/kube-proxy-7df8z                           0/1     CrashLoopBackOff   26 (38s ago)     156m    192.168.1.52   neuralserver02   <none>           <none>
kube-system   pod/kube-proxy-bcn8l                           0/1     CrashLoopBackOff   36 (2m8s ago)    3h25m   192.168.1.51   neuralserver     <none>           <none>
kube-system   pod/kube-proxy-ffxw2                           1/1     Running            136 (67m ago)    3d1h    192.168.1.55   neuralserver05   <none>           <none>
kube-system   pod/kube-proxy-zjnn8                           1/1     Running            27 (5m53s ago)   156m    192.168.1.53   neuralserver03   <none>           <none>
kube-system   pod/kube-scheduler-neuralserver05              1/1     Running            187 (67m ago)    3d1h    192.168.1.55   neuralserver05   <none>           <none>

NAMESPACE     NAME                 TYPE        CLUSTER-IP   EXTERNAL-IP   PORT(S)                  AGE    SELECTOR
default       service/kubernetes   ClusterIP   10.96.0.1    <none>        443/TCP                  3d1h   <none>
kube-system   service/kube-dns     ClusterIP   10.96.0.10   <none>        53/UDP,53/TCP,9153/TCP   3d1h   k8s-app=kube-dns

NAMESPACE     NAME                         DESIRED   CURRENT   READY   UP-TO-DATE   AVAILABLE   NODE SELECTOR            AGE    CONTAINERS    IMAGES                               SELECTOR
kube-system   daemonset.apps/calico-node   5         5         0       5            0           kubernetes.io/os=linux   3d1h   calico-node   docker.io/calico/node:v3.26.1        k8s-app=calico-node
kube-system   daemonset.apps/kube-proxy    5         5         3       5            3           kubernetes.io/os=linux   3d1h   kube-proxy    registry.k8s.io/kube-proxy:v1.28.5   k8s-app=kube-proxy

NAMESPACE     NAME                                      READY   UP-TO-DATE   AVAILABLE   AGE    CONTAINERS                IMAGES                                      SELECTOR
kube-system   deployment.apps/calico-kube-controllers   1/1     1            1           3d1h   calico-kube-controllers   docker.io/calico/kube-controllers:v3.26.1   k8s-app=calico-kube-controllers
kube-system   deployment.apps/coredns                   2/2     2            2           3d1h   coredns                   registry.k8s.io/coredns/coredns:v1.10.1     k8s-app=kube-dns

NAMESPACE     NAME                                                 DESIRED   CURRENT   READY   AGE    CONTAINERS                IMAGES                                      SELECTOR
kube-system   replicaset.apps/calico-kube-controllers-7ddc4f45bc   1         1         1       3d     calico-kube-controllers   docker.io/calico/kube-controllers:v3.26.1   k8s-app=calico-kube-controllers,pod-template-hash=7ddc4f45bc
kube-system   replicaset.apps/coredns-5dd5756b68                   2         2         2       3d1h   coredns                   registry.k8s.io/coredns/coredns:v1.10.1     k8s-app=kube-dns,pod-template-hash=5dd5756b68
```

"""
