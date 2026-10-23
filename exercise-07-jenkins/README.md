# Exercise 07 — Jenkins Installation

## Objective
Run Jenkins LTS in Docker with persistent storage, complete the initial setup, create a Freestyle job that runs shell commands, and verify a successful build.

## Technologies Used
- Jenkins LTS (`jenkins/jenkins:lts-jdk17`)
- Docker Desktop (Linux containers)
- Named Docker volume for persistence

## Prerequisites
- Docker Desktop running
- Port 8081 free

## Step-by-Step Commands

### 1. Start Jenkins
```powershell
docker run -d --name ex07-jenkins -p 8081:8080 -p 50000:50000 -v jenkins_home:/var/jenkins_home jenkins/jenkins:lts-jdk17
```
If the container already exists:
```powershell
docker start ex07-jenkins
```

### 2. Get the initial admin password
```powershell
docker exec ex07-jenkins cat /var/jenkins_home/secrets/initialAdminPassword
```

### 3. Complete setup in the browser
1. Open http://localhost:8081
2. Paste the initial admin password
3. Click **Install suggested plugins**
4. Create the first admin user
5. Accept the default Jenkins URL

### 4. Create a Freestyle job
1. **New Item** → name `hello-devops` → **Freestyle project** → OK
2. **Build Steps** → **Add build step** → **Execute shell**:
```
echo "Build number: $BUILD_NUMBER"
date
echo "Hello Jenkins"
```
3. **Save** → **Build Now**
4. Open the build → **Console Output**

## Configuration Explanation
- `-p 8081:8080` maps Jenkins' web port to 8081 on the host.
- `-p 50000:50000` is the port for inbound build agents.
- `-v jenkins_home:/var/jenkins_home` stores Jenkins data in a named volume, so jobs and settings survive container restarts.

## Actual Observed Results
Job `hello-devops`, build #1 console output:

```
Started by user admin
Running as SYSTEM
Building in workspace /var/jenkins_home/workspace/hello-devops
+ echo Build number: 1
Build number: 1
+ date
Tue Oct 20 18:13:33 UTC 2026
+ echo Hello Jenkins
Hello Jenkins
Finished: SUCCESS
```

Jenkins version: 2.541.3.

## Troubleshooting

| Problem | Fix |
|---|---|
| Can't get the password | Wait 30 to 60 seconds for Jenkins to initialize |
| Jenkins is slow or Docker stops | Close other apps, keep Minikube stopped, and give Docker more memory |
| Port 8081 already in use | Stop the other service or change the host port |

## Key Concepts
- **Jenkins:** an automation server for CI/CD.
- **Freestyle job:** a simple job configured through the UI with build steps.
- **Named volume:** persistent storage that outlives the container.

## Viva Questions

**Q1: Why use a named volume for Jenkins?**
So jobs, plugins and settings are kept when the container is stopped or recreated.

**Q2: What is `initialAdminPassword` for?**
It unlocks Jenkins on first start, so only someone with access to the server can finish the setup.

**Q3: What is a Freestyle project?**
A basic Jenkins job type configured through the UI, with build steps like "Execute shell".

**Q4: What does port 50000 do?**
It is used by inbound agents to connect to the Jenkins controller.

## Conclusion
Jenkins LTS ran in Docker with a persistent volume. After completing the setup wizard, the Freestyle job `hello-devops` ran its shell commands and finished with `Finished: SUCCESS`.