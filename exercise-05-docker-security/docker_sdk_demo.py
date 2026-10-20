"""
Exercise 05 - Docker Security Demonstration
Python Docker SDK demonstration of container management operations.

Note: AppArmor is a Linux Security Module (LSM) that is NOT enforced on 
Windows/Docker Desktop with WSL2 backend. This script demonstrates the 
Docker SDK operations and AppArmor profile structure without claiming enforcement.
"""
import docker
import time
import sys


def demonstrate_docker_sdk():
    """Demonstrate Docker SDK operations: list, start, exec, logs, remove."""
    print("=" * 60)
    print("Exercise 05 — Docker Python SDK Demonstration")
    print("=" * 60)
    
    # Connect to Docker daemon
    try:
        client = docker.from_env()
        client.ping()
        print("[OK] Connected to Docker daemon")
    except Exception as e:
        print(f"[ERROR] Cannot connect to Docker: {e}")
        sys.exit(1)
    
    # 1. List running containers
    print("\n--- 1. Running Containers ---")
    containers = client.containers.list()
    if containers:
        for c in containers:
            print(f"  {c.name}: {c.image.tags} [{c.status}]")
    else:
        print("  No containers currently running")
    
    # 2. Start a temporary Alpine container
    print("\n--- 2. Starting temporary Alpine container ---")
    temp_container = client.containers.run(
        "alpine:latest",
        name="ex05-temp-demo",
        command="sleep 30",
        detach=True,
        remove=False,
        security_opt=["no-new-privileges"],   # Security hardening
    )
    print(f"  Container started: {temp_container.name} (ID: {temp_container.short_id})")
    time.sleep(1)  # Brief wait for startup
    
    # 3. Execute a command inside the container
    print("\n--- 3. Executing command in container ---")
    try:
        exit_code, output = temp_container.exec_run(
            "sh -c 'echo Hello from inside container && hostname && date'"
        )
        print(f"  Exit code: {exit_code}")
        print(f"  Output: {output.decode().strip()}")
    except Exception as e:
        print(f"  [WARNING] exec failed: {e}")
    
    # 4. Read container logs
    print("\n--- 4. Container Logs ---")
    logs = temp_container.logs(tail=10).decode()
    print(f"  Logs: {logs.strip() or '(no stdout yet)'}")
    
    # 5. Inspect security options
    print("\n--- 5. Container Security Options ---")
    temp_container.reload()
    host_config = temp_container.attrs.get('HostConfig', {})
    security_opt = host_config.get('SecurityOpt', [])
    print(f"  SecurityOpt: {security_opt}")
    
    cap_add = host_config.get('CapAdd')
    cap_drop = host_config.get('CapDrop')
    print(f"  CapAdd: {cap_add}")
    print(f"  CapDrop: {cap_drop}")
    
    # 6. Safely stop and remove container
    print("\n--- 6. Cleanup ---")
    temp_container.stop(timeout=5)
    temp_container.remove()
    print(f"  Container {temp_container.name} stopped and removed.")
    
    print("\n[DONE] Docker SDK demonstration complete.")
    
    # AppArmor status note
    print("\n--- AppArmor Status (Windows/WSL2 note) ---")
    print("  AppArmor is NOT enforced on Windows Docker Desktop (WSL2 driver).")
    print("  AppArmor is a Linux kernel feature active only on native Linux hosts.")
    print("  The profile below is provided for reference/documentation purposes.")


if __name__ == "__main__":
    demonstrate_docker_sdk()
