# DevOps Learning and Lab Manual

This repository contains the implementation and documentation of 10 DevOps laboratory exercises.

**Student:** rohitshivakumaris23
**Repository:** https://github.com/rohitshivakumaris23/devops-labs

## Technologies
- Git and GitHub
- Docker and Docker Compose
- Kubernetes and Minikube
- Python and Flask
- MySQL and Redis
- Prometheus and Grafana
- Jenkins CI/CD
- Linux and WSL2

## Laboratory Exercises

| No. | Exercise | Status |
|---|---|---|
| 01 | Kubernetes Deployment and Service | Completed |
| 02 | Dockerized Flask on Minikube | Completed |
| 03 | ReplicaSet Scaling and Self-Healing | Completed |
| 04 | Docker Networking with MySQL and Redis | Completed |
| 05 | Docker Security and Python SDK | Completed (AppArmor profile written, not enforced) |
| 06 | Prometheus and Grafana Monitoring | Completed (alert rules loaded, none triggered) |
| 07 | Jenkins Installation and CI Job | Completed |
| 08 | Jenkins and GitHub Integration | Completed |
| 09 | Jenkins Multistage Pipeline | Completed |
| 10 | Multinode Kubernetes | Completed |

## Verification Highlights
- Flask applications were tested with HTTP requests and pytest.
- ReplicaSet scaling and self-healing were demonstrated.
- Flask, MySQL and Redis containers were healthy, and the app reported both MySQL and Redis connected.
- The Docker Python SDK managed containers (start, exec, logs, remove).
- Prometheus scraped the Flask metrics endpoint (target UP).
- The Grafana dashboard showed request metrics.
- Jenkins Freestyle job `hello-devops` completed successfully (build #1).
- Jenkins `ex08-github-ci` cloned the GitHub repository, and build #2 started automatically after a push (SCM polling).
- Jenkins five-stage pipeline `ex09-pipeline` succeeded on build #5, with 3 tests passed and `/health` returning healthy.
- Three-node Minikube cluster reached Ready status.
- `service-alpha` (nginx): 2/2 replicas Ready.
- `service-beta` (httpd): 2/2 replicas Ready.
- Both services answered from inside the cluster, and their pods were spread across the two worker nodes.

## Important Notes
- AppArmor enforcement was not available in the Docker Desktop/WSL2 environment.
- Jenkins runs on a local PC that GitHub cannot reach, so SCM polling (`H/2 * * * *`) was used instead of webhooks.
- `service-alpha` and `service-beta` are demonstration nginx and httpd workloads.
- Prometheus alert rules were loaded and stayed Inactive. No alert was triggered.
- The Grafana datasource was added manually through the Grafana interface during the run.
- The Jenkins image has no Python, so Python was installed inside the container for Exercise 09. The problems and fixes are in the Ex09 README.
- Passwords in the `docker-compose.yml` files are demo values for local lab use only.

## Repository Structure
```
devops-labs/
├── exercise-01-kubernetes/
├── exercise-02-minikube-flask/
├── exercise-03-replicaset/
├── exercise-04-docker-networking/
├── exercise-05-docker-security/
├── exercise-06-monitoring/
├── exercise-07-jenkins/
├── exercise-08-jenkins-github/
├── exercise-09-jenkins-pipeline/
├── exercise-10-multinode-kubernetes/
└── README.md
```
Each exercise has its own directory containing the source code, configuration files, Kubernetes manifests or Jenkinsfile, and a README with commands, observed results, troubleshooting and viva questions.

## Conclusion
All 10 laboratory exercises have been implemented and documented, with execution results and known limitations recorded.