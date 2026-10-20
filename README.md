# DevOps Laboratory Exercises

**Student:** rohitshivakumaris23  
**Course:** DevOps Laboratory  
**Environment:** Windows 11, Docker Desktop 4.96 (WSL2), Minikube v1.39.0, Python 3.13, kubectl

---

## Repository Structure

```
devops-labs/
├── exercise-01-kubernetes/         # Kubernetes Deployment + Service
├── exercise-02-minikube-flask/     # Flask on Minikube with unit tests
├── exercise-03-replicaset/         # ReplicaSet scaling + self-healing
├── exercise-04-docker-networking/  # Flask + MySQL + Redis via Docker Compose
├── exercise-05-docker-security/    # Docker Security + Python SDK demo
├── exercise-06-monitoring/         # Prometheus + Grafana + Flask metrics
├── exercise-07-jenkins/            # Jenkins LTS in Docker
├── exercise-08-jenkins-github/     # Jenkins + GitHub SCM polling
├── exercise-09-jenkins-pipeline/   # Declarative Jenkinsfile (5 stages)
├── exercise-10-multinode-kubernetes/ # 3-node Minikube cluster
└── README.md                       # This file
```

---

## Exercise Summary

| # | Title | Key Technology | Status |
|---|---|---|---|
| 01 | Kubernetes Basics | nginx:alpine, Deployment, NodePort | ✅ PASS |
| 02 | Flask on Minikube | Flask, Docker, pytest, Kubernetes | ✅ PASS |
| 03 | Kubernetes ReplicaSet | ReplicaSet, scaling, self-healing | ✅ PASS |
| 04 | Docker Networking | Flask + MySQL 8.0 + Redis, Compose | ✅ PASS |
| 05 | Docker Security | Python Docker SDK, AppArmor profile | ✅ PASS |
| 06 | Prometheus + Grafana | prometheus-client, PromQL, Grafana | ✅ PASS |
| 07 | Jenkins Installation | Jenkins LTS, Docker, port 8081 | ✅ PASS (manual setup) |
| 08 | Jenkins GitHub | SCM polling, Jenkinsfile, Git | ⚠️ BLOCKED (needs GitHub URL) |
| 09 | Jenkins Pipeline | 5-stage declarative pipeline, pytest | ⚠️ BLOCKED (needs GitHub URL) |
| 10 | Multi-Node Kubernetes | 3-node Minikube, 2 microservices | ✅ PASS |

---

## Quick Start

### Prerequisites
```powershell
# Verify tools
docker version
minikube status
kubectl version --client
python --version
git --version
```

### Kubernetes Exercises (01–03, 10)
```powershell
# Exercises 01, 02, 03 deploy to existing minikube cluster
kubectl get pods -A

# Exercise 10: 3-node cluster
kubectl get nodes
```

### Docker Compose Exercises (04, 06)
```powershell
# Exercise 04: Flask + MySQL + Redis
docker compose -f exercise-04-docker-networking/docker-compose.yml up -d

# Exercise 06: Flask + Prometheus + Grafana
docker compose -f exercise-06-monitoring/docker-compose.yml up -d
```

### Jenkins (07–09)
```powershell
# Check Jenkins is running
docker ps --filter name=ex07-jenkins
# Access: http://localhost:8081
```

---

## Technology Stack

```
┌─────────────────────────────────────────────────┐
│            Container Orchestration               │
│  Minikube (3-node) → kubectl → Kubernetes 1.37  │
├─────────────────────────────────────────────────┤
│              Container Runtime                   │
│  Docker Desktop 4.96 (WSL2 / Linux containers)  │
├─────────────────────────────────────────────────┤
│                  Applications                    │
│  Flask 3.0.3 · Nginx:Alpine · MySQL 8.0 · Redis │
├─────────────────────────────────────────────────┤
│                CI/CD Pipeline                    │
│  Jenkins LTS (port 8081) · Jenkinsfile · pytest │
├─────────────────────────────────────────────────┤
│                  Monitoring                      │
│  Prometheus · Grafana · prometheus-client        │
└─────────────────────────────────────────────────┘
```

---

## Running Services (After Full Setup)

| Service | URL | Notes |
|---|---|---|
| nginx-service (Ex01) | via `minikube service nginx-service --url` | NodePort 30001 |
| flask-service (Ex02) | via `minikube service flask-service --url` | NodePort 30002 |
| flask-rs-service (Ex03) | via `minikube service flask-rs-service --url` | NodePort 30003 |
| Flask+MySQL+Redis (Ex04) | http://localhost:5004 | Docker Compose |
| Flask Metrics App (Ex06) | http://localhost:5006 | Docker Compose |
| Prometheus (Ex06) | http://localhost:9090 | Docker Compose |
| Grafana (Ex06) | http://localhost:3000 | admin/admin123 |
| Jenkins (Ex07) | http://localhost:8081 | Initial password in Ex07 README |

---

## Git Commit Plan

```bash
git init
git add .
git commit -m "feat: exercise 01 - kubernetes nginx deployment"
git commit -m "feat: exercise 02 - flask minikube with unit tests"
git commit -m "feat: exercise 03 - replicaset scaling and self-healing"
git commit -m "feat: exercise 04 - docker networking flask mysql redis"
git commit -m "feat: exercise 05 - docker security sdk demo"
git commit -m "feat: exercise 06 - prometheus grafana monitoring"
git commit -m "feat: exercise 07 - jenkins lts installation"
git commit -m "feat: exercise 08 - jenkins github integration"
git commit -m "feat: exercise 09 - jenkins declarative pipeline"
git commit -m "feat: exercise 10 - multinode kubernetes cluster"
```

---

## Key Learnings

1. **Kubernetes self-healing** — ReplicaSet automatically replaces deleted pods
2. **imagePullPolicy: Never** — Required for locally built images in Minikube
3. **Docker DNS** — Containers on the same network can reach each other by service name
4. **Prometheus metrics types** — Counter (monotonic), Gauge (bidirectional), Histogram (distribution)
5. **Jenkins as code** — Declarative Jenkinsfile enables reproducible CI/CD pipelines
6. **AppArmor** — Linux-only security feature; not enforced on Windows/WSL2 Docker Desktop
7. **minikube node add** — Extends existing cluster without deleting and recreating

---

*Last Updated: October 2026*
