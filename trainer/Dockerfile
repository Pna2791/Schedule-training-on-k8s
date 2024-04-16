# FROM python:3.9-slim
FROM pytorch/pytorch


WORKDIR /training-service

# COPY requirements.txt .
# RUN pip install -r requirements.txt

# RUN pip install torch==2.2.0 torchvision==0.17.0 torchaudio==2.2.0 --index-url https://download.pytorch.org/whl/cpu
RUN pip install minio==7.2.5

COPY model.py .
COPY trainer.py .



ENTRYPOINT ["python", "trainer.py", "--id", "1"]
