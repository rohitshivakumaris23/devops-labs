# Exercise 10 — Multi-Node Kubernetes

## Objective
Create a three-node Minikube cluster (1 control-plane and 2 workers), deploy two example microservices, and verify pod distribution across nodes, replica readiness, rollout status and service connectivity.

## Technologies Used
- Minikube v1.39.0 (Docker driver) and kubectl v1.34.1
- Kubernetes v1.37.0, containerd 2.3.4
- `service-alpha`: nginx:alpine
- `service-beta`: httpd:alpine
- NodePort Services

## Prerequisites
- Docker Desktop running (Linux containers)
- Single-node Minikube cluster already created
- Enough free memory: stop Jenkins and Compose stacks first

## Project Structure
```
exercise-10-multinode-kubernetes/
├── service-alpha.yaml   # Deployment (2 replicas) + NodePort Service 30010
├── service-beta.yaml    # Deployment (2 replicas) + NodePort Service 30011
├── evidence.txt         # Captured kubectl output from the real run
└── README.md
```

## Step-by-Step Commands

### 1. Add worker nodes to the existing cluster
```powershell
minikube node add
minikube node add
kubectl get nodes
```
Wait until all three nodes show `Ready`.

### 2. Deploy the two services
```powershell
cd E:\devops-labs\exercise-10-multinode-kubernetes
kubectl apply -f service-alpha.yaml
kubectl apply -f service-beta.yaml
```

### 3. Verify
```powershell
kubectl get pods -o wide
kubectl get deployments
kubectl rollout status deployment/service-alpha
kubectl rollout status deployment/service-beta
kubectl get svc
```

### 4. Test service connectivity from inside the cluster
```powershell
kubectl run curltest --rm -it --image=busybox --restart=Never -- wget -qO- http://service-alpha-svc
kubectl run curltest2 --rm -it --image=busybox --restart=Never -- wget -qO- http://service-beta-svc
```

### 5. Save evidence
```powershell
kubectl get nodes -o wide > evidence.txt
kubectl get pods -o wide >> evidence.txt
kubectl get deployments >> evidence.txt
kubectl get svc >> evidence.txt
```

## Configuration Explanation
- **Three nodes:** one control-plane (`minikube`) and two workers (`minikube-m02`, `minikube-m03`).
- **Deployments with 2 replicas:** the scheduler spreads the pods across the available workers.
- **NodePort services:** expose each service on a fixed port (30010 and 30011) and load-balance across its pods.
- **In-cluster test:** a temporary busybox pod calls the service by its DNS name, which proves service discovery and routing.

## Actual Observed Results

**Nodes** (`kubectl get nodes -o wide`):
```
NAME           STATUS   ROLES           VERSION   INTERNAL-IP    CONTAINER-RUNTIME
minikube       Ready    control-plane   v1.37.0   192.168.49.2   containerd://2.3.4
minikube-m02   Ready    <none>          v1.37.0   192.168.49.3   containerd://2.3.4
minikube-m03   Ready    <none>          v1.37.0   192.168.49.4   containerd://2.3.4
```

**Pod distribution** (new services only, from `kubectl get pods -o wide`):
```
service-alpha-7668548695-87bkw   1/1   Running   10.244.2.2   minikube-m03
service-alpha-7668548695-d59jd   1/1   Running   10.244.1.2   minikube-m02
service-beta-6dfd756d5-4r76p     1/1   Running   10.244.1.3   minikube-m02
service-beta-6dfd756d5-5kh8q     1/1   Running   10.244.2.3   minikube-m03
```
Each service has one pod on each worker node.

**Replica readiness** (`kubectl get deployments`):
```
NAME            READY   UP-TO-DATE   AVAILABLE
service-alpha   2/2     2            2
service-beta    2/2     2            2
```

**Rollout status:**
```
deployment "service-alpha" successfully rolled out
deployment "service-beta" successfully rolled out
```

**Services** (`kubectl get svc`):
```
service-alpha-svc   NodePort   10.102.75.47    80:30010/TCP
service-beta-svc    NodePort   10.108.71.235   80:30011/TCP
```

**Service connectivity** (from a temporary busybox pod):
- `http://service-alpha-svc` returned the nginx page: "Welcome to nginx!"
- `http://service-beta-svc` returned the Apache page: "It works!"

Notes:
- The earlier exercise pods (nginx, flask, replicaset) run on the control-plane node and show 1 restart. This is because Docker Desktop was restarted during the session.
- The full `kubectl` output is saved in `evidence.txt`.

## Troubleshooting

| Problem | Fix |
|---|---|
| `kubectl` timeouts or `TLS handshake timeout` | Docker is out of memory. Stop other containers, restart Docker Desktop, then run `minikube start` |
| New node shows `NotReady` | Wait 1 to 2 minutes while the network pods start on it |
| Adding the third node is very slow | The node image is about 1.9 GB. Free memory and wait for the pull |
| `rollout status deployment/<name>` fails | Use the real name from `kubectl get deployments` |
| NodePort not reachable from Windows | With the Docker driver use `minikube service <name> --url` and keep that terminal open, or test from inside the cluster |
| `ErrImageNeverPull` with local images | Load the image into all nodes with `minikube image load <image>`, or use a public image |

## Key Concepts
- **Control-plane vs worker node:** the control plane runs the API server and scheduler, workers run the pods.
- **Scheduler:** places pods on nodes based on available resources.
- **Deployment:** manages replica pods and rolling updates.
- **NodePort service:** exposes a service on a port of every node and balances traffic across pods.
- **Cluster DNS:** pods reach services by name, such as `service-alpha-svc`.

## Viva Questions

**Q1: How did you add nodes to Minikube?**
With `minikube node add`, which creates a new node container and joins it to the existing cluster.

**Q2: How do you check which node a pod runs on?**
`kubectl get pods -o wide` shows the NODE column.

**Q3: Why are the pods spread over different nodes?**
The Kubernetes scheduler balances pods across schedulable nodes, so each service got one pod per worker.

**Q4: What does `kubectl rollout status` show?**
Whether a Deployment has finished rolling out and all its replicas are updated and available.

**Q5: What is a NodePort service?**
A service that opens a fixed port (30000 to 32767) on every node and forwards traffic to the matching pods.

**Q6: How did you verify service connectivity?**
By running a temporary busybox pod that called each service by its DNS name with `wget`.

**Q7: What happens to the pods if a worker node fails?**
The Deployment controller recreates the missing pods on the remaining healthy nodes.

**Q8: What is Pod Anti-Affinity?**
A scheduling rule that keeps replicas of the same app off the same node, which improves fault tolerance.

## Conclusion
A three-node Minikube cluster was created and two microservices (nginx:alpine and httpd:alpine) were deployed with two replicas each. The pods were spread across both worker nodes, both deployments reported 2/2 ready and rolled out successfully, and both services answered through their cluster DNS names.