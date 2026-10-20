# Exercise 05 — Docker Security

## Objective
Inspect Docker security options, create an example AppArmor security profile, and build a Python Docker SDK demonstration that lists containers, starts a temporary container, executes commands, reads logs, and safely removes the container.

## Technologies Used
- Docker Python SDK (docker==6.x)
- Docker Engine security features
- AppArmor (profile reference — not enforced on Windows/WSL2)
- Python 3.13

## Important Note on AppArmor
> **AppArmor is NOT enforced on Windows Docker Desktop with WSL2 backend.**  
> AppArmor is a Linux Security Module (LSM) that requires a native Linux kernel with AppArmor enabled. The profile in this exercise is provided as a documentation reference and would be enforced on an Ubuntu/Debian Linux host.

## Project Structure
```
exercise-05-docker-security/
├── docker_sdk_demo.py    # Python Docker SDK demonstration
├── apparmor-profile.conf # Example AppArmor profile (reference)
└── README.md
```

## Step-by-Step Commands

### 1. Install Docker SDK
```powershell
pip install docker
```

### 2. Run the SDK Demonstration
```powershell
python docker_sdk_demo.py
```

### 3. Inspect Docker Security Info (Linux host only)
```bash
# On Linux:
docker info | grep -i apparmor
docker info | grep -i seccomp
```

## Actual Observed Results

```
============================================================
Exercise 05 — Docker Python SDK Demonstration
============================================================
[OK] Connected to Docker daemon

--- 1. Running Containers ---
  minikube: ['gcr.io/k8s-minikube/kicbase@sha256:...'] [running]

--- 2. Starting temporary Alpine container ---
  Container started: ex05-temp-demo (ID: 0169a5f8b046)

--- 3. Executing command in container ---
  Exit code: 0
  Output: Hello from inside container
  0169a5f8b046
  Tue Oct 20 12:22:28 UTC 2026

--- 4. Container Logs ---
  Logs: (no stdout yet)

--- 5. Container Security Options ---
  SecurityOpt: ['no-new-privileges']
  CapAdd: None
  CapDrop: None

--- 6. Cleanup ---
  Container ex05-temp-demo stopped and removed.

[DONE] Docker SDK demonstration complete.

--- AppArmor Status (Windows/WSL2 note) ---
  AppArmor is NOT enforced on Windows Docker Desktop (WSL2 driver).
  AppArmor is a Linux kernel feature active only on native Linux hosts.
```

## AppArmor Profile Explanation
The `apparmor-profile.conf` demonstrates how to:
- Allow network TCP/UDP access
- Permit Python interpreter execution
- Allow reading the application directory
- **Deny** shell access (`/bin/bash`, `/bin/sh`)
- **Deny** package managers and download tools

## Docker Security Best Practices Demonstrated
- `security_opt: ["no-new-privileges"]` — Prevents privilege escalation
- Temporary containers for one-off tasks (removed after use)
- SDK-based container management (no shell injection risk)
- Minimal Alpine base image

## Viva Questions

**Q1: What is AppArmor?**  
AppArmor (Application Armor) is a Linux Security Module that restricts program capabilities using per-application security profiles. It works at the kernel level.

**Q2: Why is AppArmor not enforced on Docker Desktop Windows?**  
Docker Desktop on Windows uses a Linux VM via WSL2. The WSL2 kernel shipped with Docker Desktop does not have AppArmor enabled by default.

**Q3: What is `no-new-privileges` in Docker?**  
A security option that prevents container processes from gaining elevated privileges through `setuid` or `setgid` binaries.

**Q4: What are Linux capabilities in Docker?**  
Docker drops most Linux capabilities by default (e.g., `CAP_NET_RAW`, `CAP_SYS_ADMIN`). You can add with `--cap-add` or drop all with `--cap-drop=ALL`.

**Q5: What is the Python Docker SDK?**  
A Python library (`docker` package) that provides a programmatic interface to Docker Engine API for managing containers, images, volumes, and networks.

## Conclusion
Python Docker SDK demonstration executed successfully. Connected to Docker daemon, started a temporary Alpine container with `no-new-privileges` security option, executed a command, read logs, and cleaned up. AppArmor profile documented accurately — not enforced on Windows/WSL2.
