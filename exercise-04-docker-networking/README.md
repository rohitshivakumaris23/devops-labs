# Exercise 04 — Docker Networking

## Objective
Build a multi-container application with Docker Compose using Flask, MySQL and Redis. Demonstrate container networking (service discovery by name), health checks and service dependencies, and verify the application endpoint along with database and cache connectivity.

## Technologies Used
- Flask 3.0.3, redis 5.0.8, mysql-connector-python 9.0.0
- MySQL 8.0
- Redis (Alpine)
- Docker Compose with a custom bridge network

## Prerequisites
- Docker Desktop running (Linux containers)
- Ports 5004 free on the host
- Minikube stopped, to free memory (optional)

## Project Structure
```
exercise-04-docker-networking/
├── app.py               # Flask app connecting to Redis and MySQL
├── requirements.txt     # flask, redis, mysql-connector-python
├── Dockerfile           # python:3.11-slim
├── docker-compose.yml   # Three services with health checks
├── init.sql             # MySQL initialization
├── evidence.txt         # Captured output from the real run
└── README.md
```

## Step-by-Step Commands

```powershell
cd E:\devops-labs\exercise-04-docker-networking
docker compose up -d --build
docker compose ps
Invoke-RestMethod http://localhost:5004/
docker compose logs flask-app
docker compose down
```

## Configuration Explanation
- **Network:** Compose creates the bridge network `exercise-04-docker-networking_devops-network`. Docker's built-in DNS lets Flask reach `mysql` and `redis` by service name.
- **Health checks:** MySQL uses `mysqladmin ping`, Redis uses `redis-cli ping`.
- **depends_on with `condition: service_healthy`:** Flask starts only after MySQL and Redis are healthy.
- **Volume `mysql-data`:** keeps database files between runs. `docker compose down` does not delete it.
- **Credentials:** the passwords in `docker-compose.yml` are demo values for this lab only.

## Verification Commands
```powershell
docker compose ps
docker exec ex04-redis redis-cli ping
docker network inspect exercise-04-docker-networking_devops-network
```

## Actual Observed Results

`docker compose up -d --build` finished with all three containers healthy or started:
```
 ✔ Container ex04-redis   Healthy
 ✔ Container ex04-mysql   Healthy
 ✔ Container ex04-flask   Started
```

`docker compose ps`:
```
NAME         IMAGE                                     SERVICE     STATUS                    PORTS
ex04-flask   exercise-04-docker-networking-flask-app   flask-app   Up (healthy)              0.0.0.0:5004->5000/tcp
ex04-mysql   mysql:8.0                                 mysql       Up (healthy)              3306/tcp, 33060/tcp
ex04-redis   redis:alpine                              redis       Up (healthy)              6379/tcp
```

`Invoke-RestMethod http://localhost:5004/`:
```
database                 message                redis     visit_count
--------                 -------                -----     -----------
connected (MySQL 8.0.46) Docker Networking Demo connected           1
```

MySQL and Redis were both reachable from Flask over the Docker network, and the visit counter was served by Redis.

`docker compose down` removed the three containers. Docker reported a harmless error deleting the network at that moment, and the network was gone afterwards.

## Troubleshooting

| Problem | Fix |
|---|---|
| `failed to connect to the docker API` | Docker Desktop is not running. Start it and wait for "Engine running" |
| Flask exits at start | MySQL was not healthy yet. Wait and run `docker compose up -d` again |
| `Network ... Error` on `docker compose down` | Harmless. Run `docker network ls` to confirm the network is gone |
| Port 5004 already in use | Stop the other process or change the host port in `docker-compose.yml` |

## Key Concepts
- **Bridge network:** a private network where containers talk to each other by name.
- **Service discovery:** Docker DNS resolves service names to container IPs.
- **Health check:** a command Docker runs to decide whether a container is healthy.
- **depends_on with service_healthy:** controls start order based on health.

## Viva Questions

**Q1: How do containers communicate by service name in Docker Compose?**
Compose creates a custom bridge network with built-in DNS, so containers reach each other by service name, such as `mysql` and `redis`, instead of IP addresses.

**Q2: What does `depends_on` with `condition: service_healthy` do?**
It makes Flask wait until MySQL and Redis pass their health checks, which avoids connection errors at startup.

**Q3: What is a Docker bridge network?**
A private network on the host. Containers on it can reach each other by name and are isolated from other networks.

**Q4: How is `init.sql` used?**
The MySQL image runs SQL files in `/docker-entrypoint-initdb.d/` on first start, to create tables and seed data.

**Q5: How would you scale Flask to 3 instances?**
Remove `container_name` and the fixed host port, then run `docker compose up --scale flask-app=3 -d`.

**Q6: Why does `docker compose down` keep your data?**
It removes containers and networks but not named volumes, unless you add `-v`.

## Conclusion
The Flask, MySQL and Redis stack ran with Docker Compose. All three containers became healthy, and the app on port 5004 reported MySQL 8.0.46 connected, Redis connected and a visit count of 1.