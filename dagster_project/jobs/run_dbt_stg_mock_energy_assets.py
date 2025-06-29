from dagster import op, job
from dagster_dbt import DbtCliResource

@op(required_resource_keys={"dbt"})
def run_dbt_stg_mock_energy_assets_op(context):
    # Start the dbt CLI invocation
    invocation = context.resources.dbt.cli(
        ["run", "--select", "stg_mock_energy_assets"],
        context=context,
    )
    
    # Wait for the result
    invocation.wait()

    # Use .success to check if it succeeded
    if not invocation.success:
        raise Exception("❌ dbt run failed.")
    else:
        context.log.info("✅ dbt run succeeded.")

@job
def run_dbt_stg_mock_energy_assets():
    run_dbt_stg_mock_energy_assets_op()