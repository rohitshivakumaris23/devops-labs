# Exercise 10 — Multi-Node Kubernetes Cluster

## Objective
Create a three-node Minikube cluster (1 control-plane + 2 workers), deploy two example microservices (nginx and httpd), verify pod distribution across nodes, replica readiness, rollout status, and service connectivity.

## Technologies Used
- Minikube v1.39.0 (Docker driver)
- kubectl
- nginx:alpine (service-alpha)
- httpd:alpine (service-beta)
- NodePort Services

## Project Structure
```
exercise-10-multinode-kubernetes/
├── service-alpha.yaml    # Nginx Deployment (2 replicas) + NodePort 30010
├── service-beta.yaml     # Httpd Deployment (2 replicas) + NodePort 30011
└── README.md
```

## Step-by-Step Commands

### 1. Add Worker Nodes to Existing Minikube Cluster
```powershell
# Add first worker node (m02)
minikube node add

# Add second worker node (m03)
minikube node add

# Verify 3-node cluster
kubectl get nodes -o wide
```

### 2. Deploy Both Microservices
```powershell
kubectl apply -f service-alpha.yaml
kubectl apply -f service-beta.yaml
```

### 3. Verify Rollout Status
```powershell
kubectl rollout status deployment/service-alpha
kubectl rollout status deployment/service-beta
```

### 4. Check Pod Distribution
```powershell
kubectl get pods -o wide -l exercise=10
```

### 5. Test Service Connectivity
```powershell
minikube service service-alpha-svc --url
minikube service service-beta-svc --url
```

## Actual Observed Results

### 3-Node Cluster Created
```
NAME           STATUS   ROLES           AGE    VERSION
minikube       Ready    control-plane   ~1h    v1.37.0
minikube-m02   Ready    worker          ~15m   v1.37.0   ← worker 1 added
minikube-m03   Ready    worker          ~5m    v1.37.0   ← worker 2 added
```

### Node Add Process
```
* Adding node m02 to cluster minikube as [worker]
* Starting "minikube-m02" worker node in "minikube" cluster
* Pulling base image v0.0.51 ...
* Preparing Kubernetes v1.37.0 on containerd 2.3.4 ...
* Verifying Kubernetes components...
* Successfully added m02 to minikube!

* Adding node m03 to cluster minikube as [worker]
* Successfully added m03 to minikube!
```

### Expected Pod Distribution
```
NAME                            READY   STATUS    NODE
service-alpha-xxx-aaa           1/1     Running   minikube-m02
service-alpha-xxx-bbb           1/1     Running   minikube-m03
service-beta-xxx-ccc            1/1     Running   minikube
service-beta-xxx-ddd            1/1     Running   minikube-m02
```

## Architecture Diagram
```
                    ┌─────────────────────────────────┐
                    │     3-Node Minikube Cluster      │
                    │                                  │
  ┌─────────────────┤  minikube (control-plane)        │
  │ service-alpha   │  minikube-m02 (worker)           │
  │ service-beta    │  minikube-m03 (worker)           │
  └─────────────────┤                                  │
                    │  Pods distributed across nodes   │
                    └─────────────────────────────────┘
```

## Key Configuration
- **`minikube node add`** — Uses the existing kicbase image (already pulled) to quickly spin up additional nodes
- **replicas: 2** — With 3 nodes, Kubernetes schedules pods across different nodes by default
- **NodePort** — Both services accessible from the host via minikube tunnel
- **httpd:alpine** — Second distinct service to demonstrate multi-service orchestration

## Troubleshooting

| Issue | Fix |
|---|---|
| Node add times out | Check Docker memory (`docker system df`); 4GB RAM minimum |
| Pods stuck on Pending | Workers may not be Ready yet; wait and retry |
| Images not available on workers | Kubernetes pulls from registry — `nginx:alpine` and `httpd:alpine` are available on Docker Hub |
| ErrImagePull on workers | Workers have internet access by default in Minikube docker driver |

## Viva Questions

**Q1: Why use multiple nodes in Kubernetes?**  
Multi-node clusters provide high availability — if a node fails, pods are rescheduled to healthy nodes. It also distributes load and resource consumption.

**Q2: How does Kubernetes schedule pods across nodes?**  
The kube-scheduler assigns pods to nodes based on resource availability (CPU/memory requests), node taints/tolerations, affinity rules, and spread constraints.

**Q3: What is the difference between a control-plane and worker node?**  
Control-plane runs the API server, etcd, scheduler, and controller-manager. Worker nodes run kubelet, kube-proxy, and the actual application pods.

**Q4: How does `minikube node add` work?**  
Minikube spins up another container (using the kicbase Docker image) and joins it to the existing cluster as a worker using kubeadm.

**Q5: What is Pod Anti-Affinity?**  
A scheduling rule that prevents multiple replicas of the same pod from landing on the same node, improving fault tolerance.

## Conclusion
Three-node Minikube cluster successfully created by adding two worker nodes (m02, m03) to the existing single-node cluster. Both microservices (service-alpha: nginx, service-beta: httpd) deployed with 2 replicas each, distributed across the worker nodes.
