# k3d cluster delete gpu-cluster
k3d cluster delete -a

k3d cluster create gpu-cluster --image=k3s-cuda --gpus=1


# wget -q -O - https://raw.githubusercontent.com/k3d-io/k3d/main/install.sh | TAG=v5.4.6 bash