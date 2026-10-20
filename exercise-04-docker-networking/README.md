# Exercise 04 — Docker Networking

## Objective
Build a multi-container application using Docker Compose with Flask, MySQL, and Redis. Demonstrate container networking (service discovery by name), health checks, service dependencies, and verify the application endpoint along with database/cache connectivity.

## Technologies Used
- Flask 3.0.3 + redis 5.0.8 + mysql-connector-python 9.0.0
- MySQL 8.0
- Redis Alpine
- Docker Compose (bridge network)

## Project Structure
```
exercise-04-docker-networking/
├── app.py               # Flask app connecting to Redis + MySQL
├── requirements.txt     # flask, redis, mysql-connector-python
├── Dockerfile           # Python:3.11-slim
├── docker-compose.yml   # Three-service stack with health checks
├── init.sql             # MySQL database initialization
└── README.md
```

## Step-by-Step Commands

### 1. Start the Stack
```powershell
docker compose up -d --build
```

### 2. Check Service Health
```powershell
docker compose ps
```

### 3. Test Application Endpoint
```powershell
Invoke-RestMethod http://localhost:5004/
Invoke-RestMethod http://localhost:5004/health
```

### 4. View Application Logs
```powershell
docker compose logs flask-app
```

### 5. Stop Stack
```powershell
docker compose down
```

## Container Network Architecture
```
devops-network (bridge)
├── ex04-mysql   (MySQL 8.0)    ← hostname: mysql
├── ex04-redis   (Redis Alpine) ← hostname: redis
└── ex04-flask   (Flask app)    ← talks to mysql:3306 and redis:6379
```

Flask connects to MySQL using hostname `mysql` and to Redis using hostname `redis` — Docker's DNS resolves these within the bridge network.

## Health Check Configuration
```yaml
mysql:
  healthcheck:
    test: ["CMD", "mysqladmin", "ping", "-h", "localhost"]
    interval: 10s, timeout: 5s, retries: 5, start_period: 30s

redis:
  healthcheck:
    test: ["CMD", "redis-cli", "ping"]
    interval: 5s, timeout: 3s, retries: 3

flask-app:
  depends_on:
    mysql: { condition: service_healthy }
    redis: { condition: service_healthy }
```

Flask only starts after both MySQL and Redis pass their health checks.

## Expected API Response
```json
{
  "message": "Docker Networking Demo",
  "visit_count": 1,
  "redis": "connected",
  "database": "connected (MySQL 8.0.xx)"
}
```

## Verification Commands
```powershell
# Check all containers running
docker compose ps

# Inspect the network
docker network inspect exercise-04-docker-networking_devops-network

# Test Redis directly
docker exec ex04-redis redis-cli ping

# Test MySQL directly
docker exec ex04-mysql mysqladmin ping -h localhost -u devops --password=devops123
```

## Viva Questions

**Q1: How do containers communicate by service name in Docker Compose?**  
Docker Compose creates a custom bridge network and configures DNS so containers can reach each other using the service name (e.g., `mysql`, `redis`) instead of IP addresses.

**Q2: What is the purpose of `depends_on` with `condition: service_healthy`?**  
It ensures the dependent service (Flask) only starts after the dependency (MySQL/Redis) has passed its health check — preventing connection errors on startup.

**Q3: What is a Docker bridge network?**  
A private internal network created by Docker. Containers on the same bridge network can communicate with each other by name, while being isolated from external networks.

**Q4: How is `init.sql` used?**  
MySQL's official image automatically runs SQL files placed in `/docker-entrypoint-initdb.d/` on first startup, creating tables and seeding data.

**Q5: How would you scale the Flask service to 3 instances?**  
Remove the `container_name` and run: `docker compose up --scale flask-app=3 -d`

## Conclusion
Docker Compose stack with Flask, MySQL 8.0, and Redis deployed using bridge networking. Service discovery works via container DNS names. Health checks ensure proper startup order. Flask increments a Redis visit counter and verifies MySQL connectivity on each request.
