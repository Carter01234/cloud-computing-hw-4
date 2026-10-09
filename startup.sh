#!/bin/bash
# GCE startup script: runs as root every time the VM boots.
 
# Pull server.py out of the instance metadata and save it on the VM
curl -s -H "Metadata-Flavor: Google" \
  "http://metadata.google.internal/computeMetadata/v1/instance/attributes/file-server-py" \
  -o /opt/file-server.py
 
# Start the server in the background so the startup script can finish
nohup python3 /opt/file-server.py > /var/log/file-server.log 2>&1 &