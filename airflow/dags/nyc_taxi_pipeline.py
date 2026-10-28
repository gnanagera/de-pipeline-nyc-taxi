from datetime import datetime

try:
    from airflow.sdk import dag, task
except ImportError:
    from airflow.decorators import dag, task

try:
    from airflow.providers.standard.operators.bash import BashOperator
except ImportError:
    from airflow.operators.bash import BashOperator

from include.pipeline import copy_s3_to_volume, ingest_month_to_s3, load_bronze

DBT_CMD = (
    "cd /usr/local/airflow/include/taxi_dbt && "
    "/usr/local/airflow/dbt_venv/bin/dbt build"
)


@dag(
    dag_id="nyc_taxi_pipeline",
    start_date=datetime(2024, 1, 1),
    schedule=None,  # manual for now; switch to "@monthly" once it works
    catchup=False,
    params={"month": "2024-04"},
    tags=["taxi", "portfolio"],
)
def nyc_taxi_pipeline():
    @task(retries=2)
    def ingest(params=None):
        ingest_month_to_s3(params["month"])

    @task(retries=2)
    def to_volume(params=None):
        copy_s3_to_volume(params["month"])

    @task(retries=1)
    def bronze():
        load_bronze()

    dbt_build = BashOperator(task_id="dbt_build", bash_command=DBT_CMD)

    ingest() >> to_volume() >> bronze() >> dbt_build


nyc_taxi_pipeline()
