
from authen import get_client

from kfp.dsl import ContainerOp, pipeline
from kfp.dsl._container_op import Container


@pipeline(
    name="Training Pipeline",
    description="A pipeline that uses a custom Docker image for training task"
)
def custom_pipeline(epochs: int = 1, gpu=None):
    tag = "gpu" if gpu else "test"

    training: Container = ContainerOp(
        name="test docker",
        image=f"anhpn19/mnist-trainer:{tag}",
        command=["python", "trainer.py", "--id", f"{id}"]
    )

    if gpu:
        training.set_gpu_limit(gpu)


class Task:
    def __init__(self) -> None:
        self.client = get_client()

    def submit_training(self, id: int):
        response = self.client.create_run_from_pipeline_func(
            pipeline_func=custom_pipeline,
            run_name=f"Training task id: {id}",
            arguments={
                "id": id
            }
        )
        print("Submit status:", response)
        print("Task id:", response.run_id)
        return response.run_id