from dagster import Definitions
from dagster_project.assets import mock_data_csv, dbt_assets
from dagster_project.jobs.generate_mock_data_job import generate_mock_data_job
from dagster_project.jobs.run_dbt_stg_mock_energy_assets import run_dbt_stg_mock_energy_assets
from dagster_project.sensors import mock_data_sensor, mock_csv_update_sensor
from dagster_dbt import DbtCliResource
from pathlib import Path

resources = {
    "dbt": DbtCliResource(
        project_dir=str(Path(__file__).resolve().parent.parent / "dbt_project"),
        profiles_dir=str(Path.home() / ".dbt"),
    )
}

defs = Definitions(
    assets=[mock_data_csv, *dbt_assets],
    jobs=[generate_mock_data_job, run_dbt_stg_mock_energy_assets],
    sensors=[mock_data_sensor, mock_csv_update_sensor],
    resources=resources
)