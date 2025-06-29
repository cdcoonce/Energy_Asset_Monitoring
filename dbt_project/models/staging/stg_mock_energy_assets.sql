-- models/staging/stg_mock_energy_assets.sql

{{ config(materialized='table') }}

SELECT
    *
FROM read_csv_auto('../data/raw/energy_asset_readings.csv')