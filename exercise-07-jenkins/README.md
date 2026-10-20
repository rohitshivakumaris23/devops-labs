# Exercise 07 — Jenkins Installation and Configuration

## Objective
Run Jenkins LTS using Docker with persistent storage on port 8081, complete the initial setup workflow, create a Freestyle job that executes shell commands, and verify a successful build.

## Technologies Used
- Jenkins LTS (jenkins/jenkins:lts-jdk17)
- Docker with named volume (`jenkins_home`)
- Docker Engine 29.9.1

## Prerequisites
- Docker Desktop running
- Port 8081 free
- `jenkins_home` Docker volume (created automatically)

## Project Structure
```
exercise-07-jenkins/
└── README.md    # Setup instructions and verification
```

## Step-by-Step Commands

### 1. Start Jenkins Container
```powershell
docker run -d `
  --name ex07-jenkins `
  -p 8081:8080 `
  -p 50000:50000 `
  -v jenkins_home:/var/jenkins_home `
  jenkins/jenkins:lts-jdk17
```

### 2. Get Initial Admin Password
```powershell
docker exec ex07-jenkins cat /var/jenkins_home/secrets/initialAdminPassword
```

### 3. Complete Setup (Browser)
1. Open http://localhost:8081
2. Enter the initial admin password
3. Install suggested plugins
4. Create an admin user

### 4. Create Freestyle Job (Browser)
1. Click "New Item"
2. Enter name: `hello-devops`
3. Select "Freestyle project" → OK
4. Under "Build Steps" → "Execute shell":
   ```bash
   echo "Hello from Jenkins Freestyle Job!"
   echo "Build Number: $BUILD_NUMBER"
   echo "Job Name: $JOB_NAME"
   date
   python3 --version || python --version
   echo "Build Complete!"
   ```
5. Click "Save" → "Build Now"

### 5. Verify Build
- Check Console Output for `Finished: SUCCESS`

## Actual Observed Results

```
Container ID   Image                       Command   Status         Ports
de037c83956a   jenkins/jenkins:lts-jdk17   ...       Up 30 seconds  0.0.0.0:8081->8080/tcp

Initial Admin Password: e73af3667cb342e8b0dc3b30aa80be0b
```

> **Manual Step Required**: Browser setup at http://localhost:8081  
> Complete plugin installation and admin user creation to finish this exercise.

## Verification Commands
```powershell
# Check container is running
docker ps --filter name=ex07-jenkins

# Check Jenkins logs
docker logs ex07-jenkins --tail=20

# Check Jenkins is responding
Invoke-WebRequest http://localhost:8081 -UseBasicParsing | Select-Object StatusCode

# Check volume
docker volume inspect jenkins_home
```

## Configuration Explanation
- **Port 8081** — External access port (mapped from container's 8080)
- **Port 50000** — Jenkins agent communication port
- **jenkins_home volume** — Persists all Jenkins data across container restarts
- **lts-jdk17** — Long-term support Jenkins with Java 17

## Troubleshooting
| Issue | Fix |
|---|---|
| Port 8081 in use | `docker stop <conflicting-container>` |
| Can't get password | Wait 30-60s for Jenkins to initialize |
| Plugins fail to install | Check network, retry installation |
| Container exits immediately | `docker logs ex07-jenkins` for startup errors |

## Viva Questions

**Q1: Why use a named volume for Jenkins?**  
Named volumes (`jenkins_home`) persist data independently of the container lifecycle. If the container is recreated, all jobs, builds, and configuration survive.

**Q2: What is the Jenkins agent port (50000) used for?**  
Port 50000 is the JNLP (Java Web Start) port used by Jenkins build agents to connect to the controller.

**Q3: What is the difference between a Freestyle job and a Pipeline job?**  
Freestyle jobs are configured via UI forms. Pipeline jobs use code (Jenkinsfile) stored in version control, enabling Infrastructure-as-Code for CI/CD.

**Q4: What is the `initialAdminPassword` for?**  
It's a one-time secret generated during Jenkins startup to protect the setup wizard from unauthorized access.

## Conclusion
Jenkins LTS container started successfully on port 8081 with named volume `jenkins_home`. Initial admin password retrieved: `e73af3667cb342e8b0dc3b30aa80be0b`. Browser setup required to complete plugin installation and create the first Freestyle job.
