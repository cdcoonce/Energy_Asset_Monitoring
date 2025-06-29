from dagster import SensorDefinition, DefaultSensorStatus, RunRequest, AssetKey, AssetSensorDefinition
from datetime import datetime, timedelta, timezone
from dagster_project.jobs.generate_mock_data_job import generate_mock_data_job
from dagster_project.assets import run_dbt_stg_mock_energy_assets


# Periodic sensor to generate mock data
def periodic_mock_data_sensor(context):
    now = datetime.now(timezone.utc)
    last_time_str = context.cursor

    if last_time_str:
        last_time = datetime.fromisoformat(last_time_str)
        elapsed = now - last_time

        if elapsed < timedelta(minutes=10):
            context.log.info(f"⏱ Skipping run. Only {elapsed.total_seconds() / 60:.2f} minutes since last run.")
            return

    context.log.info("🚀 Triggering generate_mock_data_job now.")
    yield RunRequest(
        run_key=f"mock-{now.isoformat()}",
        job_name="generate_mock_data_job"
    )
    context.update_cursor(now.isoformat())
    context.log.info(f"✅ Updated cursor to {now.isoformat()}")


mock_data_sensor = SensorDefinition(
    name="mock_data_sensor",
    evaluation_fn=periodic_mock_data_sensor,
    job_name="generate_mock_data_job",
    minimum_interval_seconds=60,
    default_status=DefaultSensorStatus.RUNNING,
)


# Sensor to trigger dbt model after CSV asset is materialized
def on_mock_data_updated(context, _event):
    context.log.info("📈 Detected update to mock CSV. Triggering dbt model stg_mock_energy_assets.")
    return [
        RunRequest(
            run_key=None, 
            job_name="run_dbt_stg_mock_energy_assets"
        )
    ]


mock_csv_update_sensor = AssetSensorDefinition(
    name="mock_csv_update_sensor",
    asset_key=AssetKey("mock_data_csv"),
    job_name="run_dbt_stg_mock_energy_assets",
    asset_materialization_fn=on_mock_data_updated,
    default_status=DefaultSensorStatus.RUNNING,
)