import os

import boto3
import requests
from databricks import sql
from databricks.sdk import WorkspaceClient

VOLUME_ROOT = "/Volumes/workspace/bronze/raw/nyc_taxi"


def ingest_month_to_s3(month: str) -> None:
    bucket = os.environ["S3_BUCKET"]
    url = f"https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_{month}.parquet"
    local = f"/tmp/yellow_{month}.parquet"
    with requests.get(url, stream=True, timeout=60) as r:
        r.raise_for_status()
        with open(local, "wb") as f:
            for chunk in r.iter_content(1024 * 1024):
                f.write(chunk)
    boto3.client("s3").upload_file(local, bucket, f"raw/nyc_taxi/month={month}/data.parquet")
    os.remove(local)


def copy_s3_to_volume(month: str) -> None:
    bucket = os.environ["S3_BUCKET"]
    local = f"/tmp/volume_{month}.parquet"
    boto3.client("s3").download_file(bucket, f"raw/nyc_taxi/month={month}/data.parquet", local)
    w = WorkspaceClient(
        host=f"https://{os.environ['DATABRICKS_HOST']}",
        token=os.environ["DATABRICKS_TOKEN"],
    )
    with open(local, "rb") as f:
        w.files.upload(f"{VOLUME_ROOT}/month={month}/data.parquet", f, overwrite=True)
    os.remove(local)


def load_bronze() -> None:
    with sql.connect(
        server_hostname=os.environ["DATABRICKS_HOST"],
        http_path=os.environ["DATABRICKS_HTTP_PATH"],
        access_token=os.environ["DATABRICKS_TOKEN"],
    ) as conn:
        with conn.cursor() as cur:
            cur.execute(
                f"""
                COPY INTO workspace.bronze.taxi_trips
                FROM '{VOLUME_ROOT}/'
                FILEFORMAT = PARQUET
                PATTERN = '*/*.parquet'
                COPY_OPTIONS ('mergeSchema' = 'true')
                """
            )
