# Exercise 08 — Jenkins and GitHub Integration

## Objective
Configure Jenkins to use a GitHub repository, create a CI job that checks out code, configure SCM polling, and verify that a new commit triggers an automatic build.

## Technologies Used
- Jenkins LTS (running on port 8081)
- Git 2.55.0
- GitHub
- SCM polling (every 2 minutes)

## Project Structure
```
exercise-08-jenkins-github/
├── Jenkinsfile    # Pipeline with SCM polling trigger
└── README.md
```

## Step-by-Step Setup

### Prerequisites
1. Jenkins running at http://localhost:8081
2. GitHub repository created with your devops-labs code
3. Git plugin installed in Jenkins (installed by default with "suggested plugins")

### 1. Create GitHub Repository
```powershell
# Push your local devops-labs to GitHub first
# (After you provide the repo URL)
git remote add origin https://github.com/YOUR_USERNAME/devops-labs.git
git push -u origin main
```

### 2. Create Pipeline Job in Jenkins (Browser)
1. Jenkins → New Item → `github-ci-pipeline` → Pipeline → OK
2. Under **Pipeline**:
   - Definition: **Pipeline script from SCM**
   - SCM: **Git**
   - Repository URL: `https://github.com/YOUR_USERNAME/devops-labs.git`
   - Branch: `*/main`
   - Script Path: `exercise-08-jenkins-github/Jenkinsfile`

### 3. Configure SCM Polling
1. Under **Build Triggers** → Check **Poll SCM**
2. Schedule: `H/2 * * * *` (every 2 minutes)
3. Click **Save**

### 4. Test Trigger
```powershell
# Make a commit and push
echo "# trigger" >> E:\devops-labs\trigger.txt
git add trigger.txt
git commit -m "ci: trigger jenkins build"
git push
```
Wait up to 2 minutes for Jenkins to detect the commit and start a build.

### 5. Verify Build
- Jenkins → `github-ci-pipeline` → Build History → Console Output
- Should show: `git checkout`, `ls -la`, `Finished: SUCCESS`

## Jenkinsfile Explanation
```groovy
triggers {
    pollSCM('H/2 * * * *')  // Check every 2 minutes for new commits
}

stages:
  Checkout  → Clones the repo from GitHub
  Verify    → Lists files, shows git log
  BuildCheck → Checks for requirements.txt
```

## SCM Polling vs Webhooks

| Feature | SCM Polling | Webhook |
|---|---|---|
| How it works | Jenkins checks GitHub periodically | GitHub notifies Jenkins on push |
| Delay | Up to poll interval (2 min) | Near-instant |
| Network requirement | Jenkins → GitHub | GitHub → Jenkins (needs public URL) |
| Suitable for | Local/lab environments | Production with public Jenkins |

> **Note**: Webhooks require Jenkins to be publicly accessible. In this lab environment, SCM polling is the practical choice.

## Viva Questions

**Q1: What is SCM polling in Jenkins?**  
Jenkins periodically queries the source control repository for new commits. If changes are found, it triggers a build.

**Q2: What is a Jenkins webhook?**  
A webhook is an HTTP callback that GitHub sends to Jenkins when a push event occurs, triggering immediate builds.

**Q3: What is the `H` in the cron expression `H/2 * * * *`?**  
`H` (hash) distributes the load across Jenkins jobs. `H/2` means "every 2 minutes, but at a consistent offset" to avoid all jobs polling at the same second.

**Q4: What credentials are needed for a private GitHub repository?**  
A GitHub Personal Access Token (PAT) added to Jenkins as a Username/Password credential, or an SSH key pair.

## Conclusion
Jenkinsfile configured with SCM polling trigger (`H/2 * * * *`). Requires GitHub repository URL to complete end-to-end verification. Once the repo URL is provided and code is pushed, Jenkins will detect commits and trigger builds automatically.

Jenkins polling test
