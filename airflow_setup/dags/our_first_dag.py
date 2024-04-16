from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.bash import BashOperator


default_args = {
    "owner": "creator phan",
    "retries": 5,
    "retry_delay": timedelta(minutes=2)
}

with DAG(
    dag_id='our_first_dag',
    default_args=default_args,
    description='This is our first dag',
    start_date=datetime(2024, 4, 16, 17), 
    # schedule_interval='@'
) as dag:
    task_1 = BashOperator(
        task_id='first_task',
        bash_command="echo Hello World"
    )