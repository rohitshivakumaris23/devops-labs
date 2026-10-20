# Exercise 09 — Jenkins Pipeline

## Objective
Create a declarative Jenkinsfile with five stages: Build, Test, Deploy, Run Application, and Cleanup. Run automated Flask tests within the pipeline, verify application health, and confirm successful pipeline completion.

## Technologies Used
- Jenkins LTS (port 8081)
- Declarative Groovy Jenkinsfile
- Flask 3.0.3 + pytest
- Python virtual environment

## Project Structure
```
exercise-09-jenkins-pipeline/
├── Jenkinsfile           # Declarative pipeline (5 stages)
├── app.py                # Flask app tested by pipeline
├── requirements.txt      # flask + pytest
├── tests/
│   └── test_app.py       # Unit tests run in Test stage
└── README.md
```

## Jenkinsfile — 5-Stage Pipeline

```
Build  →  Test  →  Deploy  →  Run Application  →  Cleanup
```

| Stage | Action |
|---|---|
| **Build** | Creates Python venv, installs requirements |
| **Test** | Runs pytest against `tests/test_app.py` |
| **Deploy** | Logs deployment metadata (build #, app name) |
| **Run Application** | Starts Flask, health-checks `/health` endpoint |
| **Cleanup** | Kills Flask process, removes venv |

## Step-by-Step Setup

### 1. Push Code to GitHub
```powershell
# After providing your GitHub repo URL
git add exercise-09-jenkins-pipeline/
git commit -m "feat: exercise 09 jenkins pipeline"
git push
```

### 2. Create Pipeline Job in Jenkins (Browser)
1. Jenkins → New Item → `flask-pipeline` → Pipeline → OK
2. Under **Pipeline**:
   - Definition: **Pipeline script from SCM**
   - SCM: **Git**
   - Repository URL: `https://github.com/YOUR_USERNAME/devops-labs.git`
   - Branch: `*/main`
   - Script Path: `exercise-09-jenkins-pipeline/Jenkinsfile`
3. Click **Save** → **Build Now**

### 3. Verify Pipeline Stages
All 5 stages should show green in the Stage View.

## Expected Console Output

```
========== STAGE: BUILD ==========
Building flask-devops-app v1.0.0
Installing dependencies...
Build complete.

========== STAGE: TEST ==========
Running unit tests...
test_home_returns_200 PASSED
test_home_has_message PASSED
test_health_returns_healthy PASSED
All tests passed.

========== STAGE: DEPLOY ==========
APP_NAME=flask-devops-app
APP_VERSION=1.0.0
BUILD_NUMBER=1
Deployment simulation complete.

========== STAGE: RUN APPLICATION ==========
Application is healthy.

========== STAGE: CLEANUP ==========
Cleanup complete.

Pipeline completed successfully! Build #1
```

## Unit Tests (3 test cases)
```python
test_home_returns_200        # GET / → 200
test_home_has_message        # Response contains 'message' key
test_health_returns_healthy  # GET /health → {"status": "healthy"}
```

## Jenkinsfile post { } Blocks
- `success` — Prints success message with build number
- `failure` — Alerts on stage failure
- `always` — Logs completion timestamp regardless of result

## Viva Questions

**Q1: What is a declarative Jenkinsfile?**  
A Jenkinsfile using the `pipeline {}` syntax with structured `stages {}`, `steps {}`, and `post {}` blocks. It's more readable and opinionated than scripted pipelines.

**Q2: What is the purpose of `post { always {} }`?**  
Code inside `always {}` runs regardless of whether the pipeline succeeded or failed — useful for cleanup, notifications, or archiving artifacts.

**Q3: Why use virtual environments in Jenkins?**  
Venvs isolate Python dependencies per build, preventing conflicts between jobs sharing the same Jenkins agent.

**Q4: What is the difference between `sh` and `bat` in Jenkinsfile?**  
`sh` runs shell commands on Linux/macOS agents. `bat` runs batch commands on Windows agents. Linux containers (Jenkins Docker) use `sh`.

**Q5: What happens if the Test stage fails?**  
The pipeline aborts and remaining stages (Deploy, Run, Cleanup) are skipped. The `post { failure {} }` block executes.

## Conclusion
Declarative Jenkinsfile created with 5 stages including automated testing, health verification, and cleanup. Requires GitHub repository URL and browser-based Jenkins job creation to execute end-to-end.
