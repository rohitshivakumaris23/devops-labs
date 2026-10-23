# Exercise 09 — Jenkins Pipeline

## Objective
Create a declarative Jenkinsfile with five stages: Build, Test, Deploy, Run Application, and Cleanup. Run automated Flask tests inside the pipeline, verify application health, and confirm successful pipeline completion.

## Technologies Used
- Jenkins LTS (Docker, port 8081)
- Declarative Groovy Jenkinsfile
- Flask 3.0.3 and pytest
- Python 3.13 virtual environment
- GitHub (SCM source for the Jenkinsfile)

## Prerequisites
- Docker Desktop running
- Jenkins container `ex07-jenkins` running with Python 3 installed inside it
- Code pushed to https://github.com/rohitshivakumaris23/devops-labs

## Project Structure
```
exercise-09-jenkins-pipeline/
├── Jenkinsfile           # Declarative pipeline (5 stages)
├── app.py                # Flask app tested by the pipeline
├── requirements.txt      # flask + pytest
├── tests/
│   └── test_app.py       # Unit tests run in the Test stage
└── README.md
```

## Pipeline Stages

```
Build  →  Test  →  Deploy  →  Run Application  →  Cleanup
```

| Stage | Action |
|---|---|
| **Build** | Creates a Python venv and installs Flask and pytest |
| **Test** | Runs pytest against `tests/test_app.py` |
| **Deploy** | Prints deployment metadata (build number, app name) |
| **Run Application** | Starts Flask in the background and health-checks `/health` |
| **Cleanup** | Stops Flask and removes the venv |

## Step-by-Step Commands

### 1. Install Python inside the Jenkins container
The default Jenkins image has no Python.
```powershell
docker exec -u root ex07-jenkins apt-get update
docker exec -u root ex07-jenkins apt-get install -y python3 python3-pip python3-venv python-is-python3
docker exec ex07-jenkins python3 --version
```

### 2. Push the code to GitHub
```powershell
cd E:\devops-labs
git add .
git commit -m "Update exercise 09"
git push
```

### 3. Create the pipeline job in Jenkins
1. Open http://localhost:8081
2. **New Item** → name `ex09-pipeline` → **Pipeline** → OK
3. Under **Pipeline**:
   - Definition: **Pipeline script from SCM**
   - SCM: **Git**
   - Repository URL: `https://github.com/rohitshivakumaris23/devops-labs.git`
   - Branch Specifier: `*/master`
   - Script Path: `exercise-09-jenkins-pipeline/Jenkinsfile`
4. **Save** → **Build Now**

## Configuration Explanation
- `agent any` runs the pipeline on the Jenkins controller.
- `dir("${TEST_DIR}")` is needed because the app and tests are in a subfolder, while Jenkins checks out the repository root.
- `python3 -m venv --without-pip venv` followed by `python3 -m pip --python venv/bin/python install ...` creates a venv and installs packages with the system pip. This was needed because `ensurepip` does not work in this Jenkins container.
- The Run Application stage retries `/health` up to 10 times, so Flask has time to start.
- `post { success / failure / always }` prints the result and a timestamp.

## Verification
Open the build in Jenkins and check **Pipeline Overview** (all five stages green) and **Console Output**.

## Actual Observed Results
Build **#5** of `ex09-pipeline`, built from commit `90554bf` ("Install deps via system pip into venv"):

```
========== STAGE: BUILD ==========
Python 3.13.5
Successfully installed ... flask-3.0.3 ... pytest-9.1.1
Build complete.

========== STAGE: TEST ==========
tests/test_app.py::TestJenkinsPipelineApp::test_health_returns_healthy PASSED [ 33%]
tests/test_app.py::TestJenkinsPipelineApp::test_home_has_message PASSED  [ 66%]
tests/test_app.py::TestJenkinsPipelineApp::test_home_returns_200 PASSED  [100%]
============================== 3 passed in 0.10s ===============================

========== STAGE: DEPLOY ==========
APP_NAME=flask-devops-app
APP_VERSION=1.0.0
BUILD_NUMBER=5
Deployment simulation complete.

========== STAGE: RUN APPLICATION ==========
{"status":"healthy"}
Application is healthy.
{"build":"5","message":"Flask app for Jenkins Pipeline","version":"1.0.0"}

========== STAGE: CLEANUP ==========
Cleanup complete.

Pipeline completed successfully! Build #5
Finished: SUCCESS
```

Builds #1 to #4 failed while the environment was being fixed (see Troubleshooting). Build #5 is the first successful run.

## Troubleshooting

| Problem | Cause | Fix |
|---|---|---|
| `python: not found` (exit 127) | Jenkins image has no Python | Installed Python with `apt-get` inside the container |
| `Segmentation fault` from `python3` | Python binary was damaged when Docker crashed mid-install | `apt-get install --reinstall python3.13 libpython3.13-stdlib libpython3.13-minimal python3.13-minimal` |
| `venvScriptspip: not found` | Jenkinsfile contained a Windows-style fallback path | Removed the Windows fallback lines |
| `./venv/bin/pip: not found` | `ensurepip` is broken, so the venv has no pip | Create the venv with `--without-pip` and install with the system pip using `--python` |

## Key Concepts
- **Declarative pipeline:** structured `pipeline { stages { } post { } }` syntax.
- **Pipeline script from SCM:** Jenkins reads the Jenkinsfile from the Git repository, so changes must be pushed before they take effect.
- **Virtual environment:** isolates Python dependencies per build.
- **Health check:** the pipeline fails if the app does not respond on `/health`.

## Viva Questions

**Q1: What is a declarative Jenkinsfile?**
A Jenkinsfile using `pipeline {}` syntax with structured `stages`, `steps` and `post` blocks. It is more readable and opinionated than a scripted pipeline.

**Q2: What does `post { always {} }` do?**
It runs whether the pipeline succeeded or failed, which is useful for cleanup and notifications.

**Q3: Why use virtual environments in Jenkins?**
They isolate Python dependencies per build and prevent conflicts between jobs.

**Q4: What is the difference between `sh` and `bat`?**
`sh` runs shell commands on Linux/macOS agents, `bat` runs batch commands on Windows agents. Jenkins in Docker is Linux, so it uses `sh`.

**Q5: What happens if the Test stage fails?**
The pipeline stops, the remaining stages are skipped, and `post { failure {} }` runs.

**Q6: Why did Jenkins not see your Jenkinsfile changes until you pushed?**
The job uses "Pipeline script from SCM", so Jenkins fetches the Jenkinsfile from GitHub on each build.

## Conclusion
A declarative Jenkins pipeline with five stages (Build, Test, Deploy, Run Application, Cleanup) ran successfully on build #5. It installed dependencies, passed 3 unit tests, confirmed `/health` returned `{"status":"healthy"}`, and cleaned up.