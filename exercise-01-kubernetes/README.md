# Exercise 01 — Kubernetes Basics: Nginx Deployment

## Objective
Deploy an Nginx web server using Kubernetes Deployment and Service manifests, verify pod readiness, service creation, and rollout status on a Minikube single-node cluster.

## Technologies Used
- Kubernetes (kubectl v1.37.0)
- Minikube v1.39.0 (Docker driver)
- Nginx Alpine container image
- YAML manifest files

## Prerequisites
- Minikube running: `minikube status`
- kubectl configured: `kubectl version --client`

## Project Structure
```
exercise-01-kubernetes/
├── deployment.yaml    # Nginx Deployment (2 replicas)
├── service.yaml       # NodePort Service (port 30001)
└── README.md
```

## Step-by-Step Commands

### 1. Apply Deployment
```powershell
kubectl apply -f deployment.yaml
```

### 2. Apply Service
```powershell
kubectl apply -f service.yaml
```

### 3. Check Rollout Status
```powershell
kubectl rollout status deployment/nginx-deployment
```

### 4. Get Service URL
```powershell
minikube service nginx-service --url
```

## Verification Commands
```powershell
# Check pods
kubectl get pods -l app=nginx -o wide

# Check service
kubectl get service nginx-service

# Check deployment details
kubectl describe deployment nginx-deployment
```

## Actual Observed Results

```
deployment.apps/nginx-deployment created
service/nginx-service created
deployment "nginx-deployment" successfully rolled out

NAME                                READY   STATUS    RESTARTS   AGE   IP
nginx-deployment-58f6485475-4wmhb   1/1     Running   0          28s   10.244.0.3
nginx-deployment-58f6485475-flt9q   1/1     Running   0          28s   10.244.0.4

NAME            TYPE       CLUSTER-IP      EXTERNAL-IP   PORT(S)        AGE
nginx-service   NodePort   10.111.68.204   <none>        80:30001/TCP   28s

Service URL: http://127.0.0.1:49755
```

## Configuration Explanation
- **replicas: 2** — Two nginx pods for availability
- **imagePullPolicy: IfNotPresent** — Uses cached nginx:alpine
- **NodePort 30001** — External access port
- **readinessProbe** — Kubernetes checks `/` before routing traffic
- **livenessProbe** — Restarts container if health check fails

## Troubleshooting
| Issue | Cause | Fix |
|---|---|---|
| `ImagePullBackOff` | No internet / wrong image name | Use `nginx:alpine` |
| Pods stuck in Pending | Resource limits too high | Check `kubectl describe pod` |
| Service not accessible | Docker driver limitation | Use `minikube service nginx-service --url` |

## Key Concepts
- **Deployment** — Manages ReplicaSets; ensures desired pod count
- **Service (NodePort)** — Exposes pods to external traffic
- **Pod** — Smallest deployable unit in Kubernetes
- **Label Selector** — Links Service to Deployment pods

## Viva Questions

**Q1: What is a Kubernetes Deployment?**  
A Deployment manages a desired state for pods and ReplicaSets. It handles rolling updates and rollbacks automatically.

**Q2: What is the difference between NodePort and ClusterIP?**  
ClusterIP is internal-only. NodePort exposes the service on each node's IP at a static port (30000-32767).

**Q3: How does Kubernetes ensure the desired number of replicas?**  
The ReplicaSet controller continuously watches pod count and creates/deletes pods to match `spec.replicas`.

**Q4: What is a readiness probe?**  
A readiness probe tells Kubernetes when a pod is ready to receive traffic. Failed probes remove the pod from load-balancing.

**Q5: What happens during a rolling update?**  
Kubernetes gradually replaces old pods with new ones, ensuring at least some pods are always available.

## Conclusion
Successfully deployed Nginx with 2 replicas using Kubernetes Deployment and NodePort Service. Both pods reached `1/1 Running` state and the service was accessible via Minikube tunnel URL.
