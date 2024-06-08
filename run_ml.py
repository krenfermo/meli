
#!/usr/bin/env python
import subprocess

def runner():
    ssh = subprocess.Popen(["sh", "./ml.command","-d","-m"],
                        stdin =subprocess.PIPE,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        universal_newlines=True,
                        bufsize=0)
 