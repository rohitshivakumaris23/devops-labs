# DevOps Laboratory Exercises

**Student:** rohitshivakumaris23
**Course:** DevOps Laboratory
**Repository:** https://github.com/rohitshivakumaris23/devops-labs

## Environment
- Windows 11, PowerShell
- Docker Desktop 4.96 (WSL2, Linux containers)
- Minikube v1.39.0, Kubernetes v1.37.0, kubectl v1.34.1
- Python 3.13, Git 2.55
- Jenkins LTS 2.541.3 (Docker, port 8081)

## Repository Structure
```
devops-labs/
├── exercise-01-kubernetes/            # Nginx Deployment + Service
├── exercise-02-minikube-flask/        # Flask on Minikube with unit tests
├── exercise-03-replicaset/            # ReplicaSet scaling + self-healing
├── exercise-04-docker-networking/     # Flask + MySQL + Redis with Docker Compose
├── exercise-05-docker-security/       # Docker security + Python Docker SDK demo
├── exercise-06-monitoring/            # Prometheus + Grafana + Flask metrics
├── exercise-07-jenkins/               # Jenkins LTS in Docker (Freestyle job)
├── exercise-08-jenkins-github/        # Jenkins + GitHub with SCM polling
├── exercise-09-jenkins-pipeline/      # Declarative Jenkinsfile (5 stages)
├── exercise-10-multinode-kubernetes/  # 3-node Minikube cluster
└── README.md
```

## Exercise Summary

| # | Title | Key Technology | Status |
|---|---|---|---|
| 01 | Kubernetes Basics | Nginx, Deployment, Service | PASS |
| 02 | Flask on Minikube | Flask, Docker, pytest, Kubernetes | PASS |
| 03 | Kubernetes ReplicaSet | ReplicaSet, scaling, self-healing | PASS |
| 04 | Docker Networking | Flask + MySQL 8.0 + Redis, Compose | PASS (all containers healthy, app reported MySQL and Redis connected) |
| 05 | Docker Security | Python Docker SDK, AppArmor profile | PASS (AppArmor profile written but not enforced on Docker Desktop) |
| 06 | Prometheus + Grafana | Flask metrics, Prometheus, Grafana | PARTIAL (stack started and containers ran; dashboard and alert state not verified) |
| 07 | Jenkins Installation | Jenkins LTS, Docker, Freestyle job | PASS (build #1: Finished: SUCCESS) |
| 08 | Jenkins + GitHub | Freestyle job, Git, SCM polling | PASS (build #2 started by an SCM change) |
| 09 | Jenkins Pipeline | Declarative pipeline, pytest | PASS (build #5: all 5 stages, 3 tests passed) |
| 10 | Multi-Node Kubernetes | 3-node Minikube, 2 microservices | PASS (pods spread across 2 workers, both services reachable) |

Each exercise folder has its own README with the commands, configuration explanation, observed results, troubleshooting and viva questions.

## Quick Start

Check the tools:
```powershell
docker --version
minikube version
kubectl version --client
python --version
git --version
```

Kubernetes exercises (01 to 03, 10):
```powershell
minikube start
kubectl get nodes
kubectl get pods
```

Docker Compose exercises (04, 06). Run one at a time and stop each when finished:
```powershell
cd exercise-04-docker-networking
docker compose up -d --build
docker compose ps
docker compose down
```

Jenkins (07 to 09):
```powershell
docker start ex07-jenkins
```
Open http://localhost:8081 and log in with the admin user created during setup.

## Services and Ports

| Service | Address | Notes |
|---|---|---|
| nginx-service (Ex01) | `minikube service nginx-service --url` | NodePort 30001 |
| flask-service (Ex02) | `minikube service flask-service --url` | NodePort 30002 |
| flask-rs-service (Ex03) | `minikube service flask-rs-service --url` | NodePort 30003 |
| Flask + MySQL + Redis (Ex04) | http://localhost:5004 | Docker Compose |
| Flask metrics app (Ex06) | http://localhost:5006 | Docker Compose |
| Prometheus (Ex06) | http://localhost:9090 | Docker Compose |
| Grafana (Ex06) | http://localhost:3000 | Demo login in the compose file |
| service-alpha / service-beta (Ex10) | NodePort 30010 / 30011 | Tested from inside the cluster |
| Jenkins (Ex07 to 09) | http://localhost:8081 | Admin user created during setup |

## Notes on the Environment
- Docker Desktop has limited memory, so the 3-node cluster, Jenkins and the Compose stacks were run one at a time.
- The Jenkins image has no Python, so Python was installed inside the container for Exercise 09. The problems met and their fixes are in the Ex09 README.
- Jenkins runs on a local PC that GitHub cannot reach, so SCM polling was used instead of a webhook.
- Passwords in the `docker-compose.yml` files are demo values for local lab use only.

## Key Learnings
- **Self-healing:** a ReplicaSet replaces deleted pods automatically.
- **Docker DNS:** containers on the same network reach each other by service name.
- **Multi-node scheduling:** the scheduler spreads pods across worker nodes.
- **Jenkins as code:** a declarative Jenkinsfile makes the pipeline reproducible.
- **SCM polling vs webhooks:** polling works when GitHub cannot reach Jenkins.
- **AppArmor:** Linux-only, so it is not enforced with Docker Desktop on Windows.