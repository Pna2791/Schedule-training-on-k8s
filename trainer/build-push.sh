tag="gpu"

docker build -t anhpn19/mnist-trainer:$tag .
docker push anhpn19/mnist-trainer:$tag

docker run anhpn19/mnist-trainer:$tag