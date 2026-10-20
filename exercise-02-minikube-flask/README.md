# Exercise 02 — Flask Application with Minikube

## Objective
Build a Flask application with `/` and `/health` endpoints, containerize it using Docker, deploy to Minikube with Kubernetes manifests, and verify with automated Python unit tests.

## Technologies Used
- Python 3.11 + Flask 3.0.3
- Docker (python:3.11-slim base image)
- Minikube v1.39.0 (Docker driver)
- pytest 9.1.1
- kubectl

## Prerequisites
- Minikube running with Docker driver
- Python 3 installed locally
- flask installed: `pip install flask`

## Project Structure
```
exercise-02-minikube-flask/
├── app.py               # Flask application (/ and /health endpoints)
├── test_app.py          # Unit tests (6 test cases)
├── requirements.txt     # flask==3.0.3
├── Dockerfile           # Python:3.11-slim, non-root user
├── k8s-deployment.yaml  # Deployment + Service (NodePort 30002)
└── README.md
```

## Step-by-Step Commands

### 1. Run Unit Tests First
```powershell
pip install flask
python -m pytest test_app.py -v
```

### 2. Build Image Inside Minikube
```powershell
# Build directly into minikube's Docker daemon (avoids ErrImageNeverPull)
minikube image build -t flask-k8s:latest .
```

### 3. Deploy to Kubernetes
```powershell
kubectl apply -f k8s-deployment.yaml
kubectl rollout status deployment/flask-deployment --timeout=60s
```

### 4. Access Application
```powershell
minikube service flask-service --url
```

## Verification Commands
```powershell
# Check pods
kubectl get pods -l app=flask-app

# Test endpoints
$URL = minikube service flask-service --url
Invoke-RestMethod "$URL/"
Invoke-RestMethod "$URL/health"
```

## Actual Observed Results

### Unit Tests (6/6 PASSED)
```
test_app.py::TestFlaskApp::test_health_endpoint_service_name PASSED
test_app.py::TestFlaskApp::test_health_endpoint_status_code PASSED
test_app.py::TestFlaskApp::test_health_endpoint_status_field PASSED
test_app.py::TestFlaskApp::test_home_endpoint_json_response PASSED
test_app.py::TestFlaskApp::test_home_endpoint_status_code PASSED
test_app.py::TestFlaskApp::test_unknown_route_returns_404 PASSED

6 passed in 0.28s
```

### Kubernetes Deployment
```
deployment "flask-deployment" successfully rolled out
NAME                               READY   STATUS    RESTARTS   AGE
flask-deployment-xxx               1/1     Running   0          30s
flask-deployment-yyy               1/1     Running   0          30s
```

## Configuration Explanation
- **imagePullPolicy: Never** — Uses the locally built image in minikube's daemon
- **readinessProbe on /health** — Traffic only routed after Flask is ready
- **Non-root user** — Security best practice in Dockerfile
- **NodePort 30002** — External access port

## Troubleshooting
| Issue | Fix |
|---|---|
| `ErrImageNeverPull` | Build with `minikube image build` not `docker build` |
| `ModuleNotFoundError: flask` | Run `pip install flask` before tests |
| Pods in `CrashLoopBackOff` | Check `kubectl logs <pod-name>` |

## Key Concepts
- **imagePullPolicy: Never** — Essential for locally built images in Minikube
- **Flask test client** — Tests HTTP responses without a real server
- **Kubernetes readiness probe** — Prevents traffic to unready pods
- **Docker layer caching** — `COPY requirements.txt` first for faster rebuilds

## Viva Questions

**Q1: Why use `minikube image build` instead of `docker build`?**  
Minikube uses its own Docker daemon inside the VM/container. `docker build` on the host creates images in the host daemon, which Kubernetes inside Minikube cannot access.

**Q2: What is `imagePullPolicy: Never`?**  
It tells Kubernetes to never pull the image from a registry and only use what's already present in the local daemon.

**Q3: What do Flask unit tests test?**  
The test client simulates HTTP requests without starting a real server, checking status codes and response body content.

**Q4: What is a /health endpoint used for?**  
Health endpoints are used by Kubernetes liveness/readiness probes to determine if a pod should receive traffic.

## Conclusion
Flask app built, unit-tested (6/6 pass), containerized, and deployed to Minikube. Kubernetes deployment rolled out successfully with 2 replicas.
