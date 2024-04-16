#!/bin/bash
set -euxo pipefail
# due to some unknown reason, copying symlinks fails with buildkit enabled
DOCKER_BUILDKIT=0 docker build \
  -t anhpn19/k3s-cuda:latest .
echo "Done!"


docker push anhpn19/k3s-cuda:latest