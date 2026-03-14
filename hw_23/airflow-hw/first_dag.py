from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator
from firstproj import runner

dag = DAG(
    "first",
    schedule="33 4 * * *",
    start_date=datetime.fromisoformat("2026-02-10T10:10:10+00:00"),
    catchup=False,
)

extract_data = PythonOperator(
    task_id="extract_data",
    python_callable=runner.extract_data,
    dag=dag,
)

extract_from_clickhouse = PythonOperator(
    task_id="extract_from_clickhouse",
    python_callable=runner.extract_from_clickhouse,
    dag=dag,
)

train = PythonOperator(
    task_id="train",
    python_callable=runner.train,
    dag=dag,
)

[extract_data, extract_from_clickhouse] >> train
