# dagster_project/jobs/generate_mock_data_job.py

from dagster import job, op
import subprocess

@op
def run_mock_data_script():
    result = subprocess.run(["python", "scripts/generate_mock_data.py"], capture_output=True, text=True)
    if result.returncode != 0:
        raise Exception(f"Script failed:\n{result.stderr}")
    print(result.stdout)

@job
def generate_mock_data_job():
    run_mock_data_script()