"""Native hook fixture: exited, orphaned session leaders must be collected."""
from pathlib import Path
import subprocess
import sys
import time


child = """
import os, time
parent = os.getpid()
pid = os.fork()
if pid == 0:
    os.setsid()
    while os.getppid() == parent:
        time.sleep(0.005)
    os._exit(0)
print(pid, flush=True)
os._exit(0)
"""
orphans = [int(subprocess.check_output([sys.executable, '-c', child], text=True))
           for _ in range(16)]
# The subprocess pipes close only after each orphan exits. Allow the subreaper
# to receive SIGCHLD and collect it; this is a fixture assertion safety limit.
deadline = time.monotonic() + 5
while any(Path(f'/proc/{pid}').exists() for pid in orphans):
    if time.monotonic() >= deadline:
        remaining = [pid for pid in orphans if Path(f'/proc/{pid}').exists()]
        raise AssertionError(f'exited orphan processes remain: {remaining}')
    time.sleep(0.01)
print(f'orphan session leaders collected: {len(orphans)}')
