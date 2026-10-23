# Exercise 08 — Jenkins and GitHub Integration

## Objective
Configure Jenkins to use a GitHub repository, create a CI job that checks out the code, configure SCM polling, and verify that a new commit triggers a build automatically.

## Technologies Used
- Jenkins LTS (Docker, port 8081)
- Git and GitHub
- Freestyle job with Git SCM
- SCM polling (`H/2 * * * *`)

## Prerequisites
- Jenkins running at http://localhost:8081 (see Exercise 07)
- Git plugin installed (included in "suggested plugins")
- Code pushed to https://github.com/rohitshivakumaris23/devops-labs (public repository, so no credentials are needed)

## Project Structure
```
exercise-08-jenkins-github/
├── Jenkinsfile    # Alternative pipeline version with a pollSCM trigger
└── README.md
```
The job that was actually run is a Freestyle job configured in the Jenkins UI.

## Step-by-Step Commands

### 1. Push the code to GitHub
```powershell
cd E:\devops-labs
git remote add origin https://github.com/rohitshivakumaris23/devops-labs.git
git push -u origin master
```

### 2. Create the Jenkins job
1. Open http://localhost:8081
2. **New Item** → name `ex08-github-ci` → **Freestyle project** → OK
3. **Source Code Management** → **Git**
   - Repository URL: `https://github.com/rohitshivakumaris23/devops-labs.git`
   - Branch Specifier: `*/master`
4. **Build Triggers** → tick **Poll SCM** → Schedule: `H/2 * * * *`
5. **Build Steps** → **Execute shell**:
```
echo "Checked out code:"
ls
git log -1 --oneline
```
6. **Save** → **Build Now**

### 3. Trigger a build with a new commit
```powershell
cd E:\devops-labs
Add-Content exercise-08-jenkins-github\README.md "`nJenkins polling test"
git add .
git commit -m "Trigger Jenkins build"
git push
```
Wait 2 to 3 minutes. Jenkins polls GitHub and starts a build by itself.

## Configuration Explanation
- **Git SCM** tells Jenkins which repository and branch to clone into the job's workspace.
- **Poll SCM** `H/2 * * * *`: Jenkins checks GitHub about every 2 minutes. The `H` spreads the exact minute across jobs to avoid load spikes.
- A build only starts if the poll finds a new commit.

## Verification
Open the job, then **Build History**, then a build, then **Console Output**. Check the first line to see what started the build.

## Actual Observed Results

**Build #1** (started manually with Build Now):
```
Started by user admin
Cloning repository https://github.com/rohitshivakumaris23/devops-labs.git
Checking out Revision e00e8f84645758458db015c5cf70643b09ff2ac3 (refs/remotes/origin/master)
Commit message: "feat: complete all 10 devops lab exercises"
+ ls
README.md
exercise-01-kubernetes
...
exercise-10-multinode-kubernetes
+ git log -1 --oneline
e00e8f8 feat: complete all 10 devops lab exercises
Finished: SUCCESS
```

**Build #2** (started automatically after the new commit was pushed):
```
Started by an SCM change
Checking out Revision 23603200d3b54469b02f70f19ba9ec8da5ec3de8 (refs/remotes/origin/master)
Commit message: "Trigger Jenkins build"
+ git log -1 --oneline
2360320 Trigger Jenkins build
Finished: SUCCESS
```

Build #2 started without clicking Build Now, so SCM polling works.

## Troubleshooting

| Problem | Fix |
|---|---|
| No build appears after pushing | Wait 2 to 4 minutes, then check the job's **Git Polling Log** |
| Git option missing in the job | Install the **Git** plugin in Manage Jenkins → Plugins |
| Authentication error on clone | Make the repo public, or add a GitHub token as a Jenkins credential |
| Branch not found | The branch is `master` here, so use `*/master`, not `*/main` |

## SCM Polling vs Webhooks

| Feature | SCM Polling | Webhook |
|---|---|---|
| How it works | Jenkins checks GitHub periodically | GitHub notifies Jenkins on push |
| Delay | Up to the poll interval (about 2 min) | Near-instant |
| Network requirement | Jenkins → GitHub | GitHub → Jenkins (needs a public URL) |
| Suitable for | Local and lab environments | Production with a reachable Jenkins |

Jenkins runs on a local PC and is not reachable from GitHub, so polling was used instead of a webhook.

## Key Concepts
- **SCM polling:** Jenkins asks the repository for changes on a schedule.
- **Webhook:** the repository calls Jenkins when a push happens.
- **Workspace:** the folder where Jenkins checks out the code.

## Viva Questions

**Q1: What is SCM polling?**
Jenkins periodically checks the repository for new commits and starts a build if it finds any.

**Q2: What is a webhook?**
An HTTP callback that GitHub sends to Jenkins on a push event, which triggers a build almost immediately.

**Q3: What does `H` mean in `H/2 * * * *`?**
`H` is a hash that picks a consistent minute per job, so not all jobs poll at the same second. `H/2` means every 2 minutes.

**Q4: Why was polling used instead of a webhook?**
Jenkins runs on a local machine that GitHub cannot reach, and webhooks need a publicly reachable URL.

**Q5: What credentials are needed for a private repo?**
A GitHub personal access token added to Jenkins as a Username/Password credential, or an SSH key.

**Q6: How did you know the second build was triggered by polling?**
The console output of build #2 starts with "Started by an SCM change", while build #1 says "Started by user admin".

## Conclusion
A Freestyle job cloned the GitHub repository and ran shell commands successfully (build #1). After pushing a new commit, SCM polling detected the change and started build #2 automatically, which also finished with `Finished: SUCCESS`.