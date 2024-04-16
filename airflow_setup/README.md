# Schedule-training-on-k8s

Download docker-compose.yaml file:

```
curl -LfO 'https://airflow.apache.org/docs/apache-airflow/2.9.0/docker-compose.yaml'
```

Create folder environment

```
mkdir -p ./dags ./logs ./plugins ./config
echo -e "AIRFLOW_UID=$(id -u)" > .env
```

Initialize the database
```
docker-compose up airflow-init
```

Running Airflow
```
docker compose up -d
```

To stop 
```
docker-compose down -v
```