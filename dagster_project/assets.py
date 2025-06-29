# dagster_project/assets.py

from dagster import asset
from dagster_dbt import dbt_cli_resource, load_assets_from_dbt_project
from pathlib import Path


@asset(required_resource_keys={"dbt"})
def run_dbt_stg_mock_energy_assets(context):
    context.log.info("Running dbt model stg_mock_energy_assets")
    context.resources.dbt.run(models=["stg_mock_energy_assets"])

@asset
def mock_data_csv():
    filepath = Path(__file__).resolve().parent.parent / "data" / "raw" / "energy_asset_readings.csv"
    assert filepath.exists()
    return filepath

dbt_assets = load_assets_from_dbt_project(
    project_dir=str(Path(__file__).resolve().parent.parent / "dbt_project"),
    profiles_dir=str(Path.home() / ".dbt")
)