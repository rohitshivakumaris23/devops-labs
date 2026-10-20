# Exercise 03 — Kubernetes ReplicaSet

## Objective
Deploy a Flask application with a Kubernetes ReplicaSet (3 replicas), scale it to 5 replicas, delete a pod and verify automatic replacement, demonstrating Kubernetes self-healing capabilities.

## Technologies Used
- Kubernetes ReplicaSet
- Flask (Python 3.11-slim Docker image)
- kubectl
- Minikube v1.39.0

## Project Structure
```
exercise-03-replicaset/
├── app.py              # Flask app exposing pod identity
├── requirements.txt    # flask==3.0.3
├── Dockerfile          # Python:3.11-slim
├── replicaset.yaml     # ReplicaSet (3 replicas) + NodePort Service
└── README.md
```

## Step-by-Step Commands

### 1. Build Image in Minikube
```powershell
minikube image build -t flask-rs:latest .
```

### 2. Deploy ReplicaSet (3 replicas)
```powershell
kubectl apply -f replicaset.yaml
kubectl get replicaset flask-replicaset
kubectl get pods -l app=flask-rs
```

### 3. Scale to 5 Replicas
```powershell
kubectl scale replicaset flask-replicaset --replicas=5
kubectl get pods -l app=flask-rs
```

### 4. Delete a Pod and Verify Self-Healing
```powershell
$pod = kubectl get pods -l app=flask-rs --no-headers -o custom-columns=":metadata.name" | Select-Object -First 1
kubectl delete pod $pod
kubectl get pods -l app=flask-rs   # New pod created automatically
```

## Actual Observed Results

### Initial 3 Pods
```
NAME                     READY   STATUS    RESTARTS   AGE
flask-replicaset-g8kq6   1/1     Running   0          65s
flask-replicaset-jjkvn   1/1     Running   0          65s
flask-replicaset-tpwtw   1/1     Running   0          65s
```

### Scaled to 5 Pods
```
NAME                     READY   STATUS    RESTARTS   AGE
flask-replicaset-94bkh   1/1     Running   0          10s  ← new
flask-replicaset-g8kq6   1/1     Running   0          75s
flask-replicaset-jjkvn   1/1     Running   0          75s
flask-replicaset-nswk4   1/1     Running   0          10s  ← new
flask-replicaset-tpwtw   1/1     Running   0          75s
```

### After Deleting Pod flask-replicaset-94bkh
```
NAME                     READY   STATUS    RESTARTS   AGE
flask-replicaset-9hl5c   1/1     Running   0          37s  ← NEW replacement!
flask-replicaset-g8kq6   1/1     Running   0          2m58s
flask-replicaset-jjkvn   1/1     Running   0          2m58s
flask-replicaset-nswk4   1/1     Running   0          113s
flask-replicaset-tpwtw   1/1     Running   0          2m58s

DESIRED: 5 | CURRENT: 5 | READY: 5  ✅
```

## Key Concepts
- **ReplicaSet** — Ensures N pods matching a label selector always run
- **Self-healing** — Controller loop recreates deleted pods automatically
- **Label Selector** — The link between RS and the pods it manages
- **Scale** — `kubectl scale` updates `spec.replicas` without downtime

## Viva Questions

**Q1: What is the difference between a ReplicaSet and a Deployment?**  
A Deployment wraps a ReplicaSet and adds rolling update and rollback capabilities. In production, always use Deployments.

**Q2: How does Kubernetes know to recreate a deleted pod?**  
The ReplicaSet controller watches pod count. When it drops below `spec.replicas`, it creates new pods.

**Q3: Can ReplicaSet pods be on different nodes?**  
Yes, Kubernetes scheduler distributes pods across available nodes unless constrained by `nodeSelector` or affinity rules.

**Q4: What happens if you delete the ReplicaSet?**  
By default, all pods it manages are also deleted. Use `--cascade=orphan` to keep pods running.

## Conclusion
ReplicaSet deployed with 3 replicas, scaled to 5, and self-healing verified: pod deletion triggered automatic replacement within seconds.
