import os
import requests
import boto3

BUCKET = os.environ["S3_BUCKET"]


def ingest(month: str):
    url = f"https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_{month}.parquet"
    local = f"/tmp/yellow_{month}.parquet"
    print(f"Downloading {month}...")
    with requests.get(url, stream=True, timeout=60) as r:
        r.raise_for_status()
        with open(local, "wb") as f:
            for chunk in r.iter_content(1024 * 1024):
                f.write(chunk)
    key = f"raw/nyc_taxi/month={month}/data.parquet"
    boto3.client("s3").upload_file(local, BUCKET, key)
    os.remove(local)
    print(f"Uploaded to s3://{BUCKET}/{key}")


if __name__ == "__main__":
    for m in ["2024-01", "2024-02", "2024-03"]:
        ingest(m)
