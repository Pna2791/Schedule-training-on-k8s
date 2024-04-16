import torch
import torch.nn as nn
import torch.optim as optim
import torchvision
import torchvision.transforms as transforms
from torch.utils.data import DataLoader
from minio import Minio

from model import Net

import logging
import json


access_key = "gvOldBjc58YjGNIxTGNx"
secret_key = "SonZwSq3sdFNFaQ3z4QVNYa9Byr6Du3mU9dO5SoW"
server_url = "anhpn.ddns.net:8022"

bucket = "mnist"

# spam = torch.rand(
#     device='cuda',
#     size=(2, 1024, 1024, 1024),
#     dtype=torch.float32
# )


logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


class Trainer:
    def __init__(self, id: int=1) -> None:
        self.device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
        self.training_id = id
        params = self.get_params()
        print("params:", params)
        self.num_epochs = params.get("epochs", 1)
        self.batch_size = params.get("batch_size", 64)

    def get_params(self) -> dict:
        self.client = Minio(
            server_url,
            access_key=access_key,
            secret_key=secret_key,
            secure=False
        )
        self.client.fget_object(
            bucket_name=bucket,
            object_name=f"training/{self.training_id}/config.json",
            file_path="config.json"
        )
        with open("config.json", "r") as f:
            return json.load(f)


    def load_model(self):
        self.model = Net().to(self.device)

        self.criterion = nn.CrossEntropyLoss()
        self.optimizer = optim.SGD(self.model.parameters(), lr=0.001, momentum=0.9)

    def load_data(self):
        # Load MNIST dataset
        transform = transforms.Compose([transforms.ToTensor(), transforms.Normalize((0.5,), (0.5,))])
        trainset = torchvision.datasets.MNIST(root='./data', train=True, download=True, transform=transform)
        self.trainloader = DataLoader(trainset, batch_size=self.batch_size, shuffle=True)


    def train(self):
        print("Start training")
        for epoch in range(self.num_epochs):
            running_loss = 0.0
            for i, data in enumerate(self.trainloader, 0):
                inputs, labels = data[0].to(self.device), data[1].to(self.device)
                self.optimizer.zero_grad()

                outputs = self.model(inputs)
                loss = self.criterion(outputs, labels)
                loss.backward()
                self.optimizer.step()

                running_loss += loss.item()
                if i % 100 == 99:
                    progress_mess = f"[{epoch + 1}/{self.num_epochs}, {i + 1}] loss: {running_loss / 100:.3f}"
                    logging.info(progress_mess)
                    running_loss = 0.0
            
        torch.save(self.model.state_dict(), 'model.pt')
        self.client.fput_object(
            bucket_name="mnist",
            object_name=f"training/{self.training_id}/model.pt",
            file_path="model.pt"
        )
        print("Trained, uploaded")



# Call the training function with the specified number of epochs
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--id", type=int, default=1, help="Training ID")
    args = parser.parse_args()


    trainer = Trainer(id=args.id)
    trainer.load_data()
    trainer.load_model()
    trainer.train()
