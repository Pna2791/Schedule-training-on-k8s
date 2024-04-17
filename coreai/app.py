from fastapi import FastAPI, Body
from pydantic import BaseModel
import json
from minio_service import minio_client
import os
from task import Task


app = FastAPI()


class TrainingParams(BaseModel):
    id: int
    epochs: int
    batch_size: int


@app.post("/train")
async def train(params: TrainingParams = Body(...)):
    """
    Train the model with provided parameters.

    Body Parameters:
        params (TrainingParams): Training parameters including epochs and batch_size.
    """

    id = params.id

    with open(f"config_{id}.json", "w") as f:
        json.dump(
            {
               "epochs": params.epochs,
               "batch_size": params.batch_size 
            }, f, indent=4)
    
    minio_client.fput_object(
        bucket_name="mnist",
        object_name=f"training/{id}/config.json",
        file_path=f"config_{id}.json"
    )
    os.remove(f"config_{id}.json")
    task_service = Task()
    task_id = task_service.submit_training(id=id)

    return {"message": f"Training Sumitted! Task ID: {task_id}"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
