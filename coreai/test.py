
import json
from pydantic import BaseModel

my_data = {
  "id": 1,
  "epochs": 1,
  "batch_size": 256
}


class TrainingParams(BaseModel):
    id: int
    epochs: int
    batch_size: int

data = TrainingParams(**my_data)

with open("config.json", "w") as f:
  json.dump(data, f, indent=4)