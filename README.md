# Santander Cycles Usage Analysis

[![License](https://img.shields.io/badge/license-MIT-blue.svg)] [![Python](https://img.shields.io/badge/python-3.8%2B-brightgreen)] [![PostgreSQL](https://img.shields.io/badge/postgresql-18%2B-blue.svg)]

In this project we explore London Santander Cycles usage statistics from [TfL Open Data](https://cycling.data.tfl.gov.uk/#!usage-stats%2F), containing information on 9M+ trips across the network, a year's worth of journey data, to understand usage patterns. A Python ingestion script loads the raw journey data into PostgreSQL, followed by an SQL transformation step that produces a clean, typed table ready for analysis.

**Status: data ingestion and transformation complete, analysis not yet started.**

## Project Overview

#### Data

The data consists of the combination of semi-monthly CSV exports of Santander Cycles journey data from [TfL Open Data](https://cycling.data.tfl.gov.uk/#!usage-stats%2F) between June 2025 and May 2026. Below is a sample from the first half of June where each row represents a single hire:

<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Number</th>
      <th>Start date</th>
      <th>Start station number</th>
      <th>Start station</th>
      <th>End date</th>
      <th>End station number</th>
      <th>End station</th>
      <th>Bike number</th>
      <th>Bike model</th>
      <th>Total duration</th>
      <th>Total duration (ms)</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>149472321</td>
      <td>2025-06-15 23:59</td>
      <td>1138</td>
      <td>Elizabeth Bridge, Victoria</td>
      <td>2025-06-16 00:13</td>
      <td>200223.0</td>
      <td>Ashmole Estate, Oval</td>
      <td>52796</td>
      <td>CLASSIC</td>
      <td>13m 59s</td>
      <td>839501.0</td>
    </tr>
    <tr>
      <th>1</th>
      <td>149472322</td>
      <td>2025-06-15 23:59</td>
      <td>300081</td>
      <td>Haggerston Road, Haggerston</td>
      <td>2025-06-16 00:05</td>
      <td>200025444.0</td>
      <td>London Fields, Hackney Central_OLD</td>
      <td>30718</td>
      <td>CLASSIC</td>
      <td>6m 19s</td>
      <td>379495.0</td>
    </tr>
    <tr>
      <th>2</th>
      <td>149472323</td>
      <td>2025-06-15 23:59</td>
      <td>22175</td>
      <td>Canton Street, Poplar</td>
      <td>2025-06-16 00:27</td>
      <td>200148.0</td>
      <td>Ansell House, Stepney</td>
      <td>59110</td>
      <td>CLASSIC</td>
      <td>28m 1s</td>
      <td>1681609.0</td>
    </tr>
    <tr>
      <th>3</th>
      <td>149472324</td>
      <td>2025-06-15 23:59</td>
      <td>200230444</td>
      <td>Maplin Street, Mile End_OLD</td>
      <td>2025-06-16 00:05</td>
      <td>200123.0</td>
      <td>Burdett Road, Mile End</td>
      <td>62747</td>
      <td>PBSC_EBIKE</td>
      <td>6m 11s</td>
      <td>371446.0</td>
    </tr>
    <tr>
      <th>4</th>
      <td>149472325</td>
      <td>2025-06-15 23:59</td>
      <td>1071</td>
      <td>Tower Gardens , Tower</td>
      <td>2025-06-16 00:18</td>
      <td>200002.0</td>
      <td>Jubilee Street, Stepney</td>
      <td>35603</td>
      <td>CLASSIC</td>
      <td>18m 45s</td>
      <td>1125297.0</td>
    </tr>
  </tbody>
</table>
</div>

Across a full year, this totals 9,093,020 rows and 1.41GB of data.

#### Ingestion

`load_data.py` reads each monthly CSV, renames columns to consistent snake_case and appends the raw rows into a `journeys_raw` staging table in PostgreSQL using SQLAlchemy. Files are loaded one at a time to avoid holding the full 1.4GB dataset in memory at once.

#### Transformation

`transform.sql` builds a clean `journeys` table from the raw data:

- Parses `start_date` and `end_date` into proper timestamps using the TIMESTAMP datatype
- Casts station numbers, bike numbers and durations to appropriate numeric/interval datatypes
- Replaces `bike_model` values into clearer labels (`CLASSIC` → `standard`, `PBSC_EBIKE` → `e-bike`)
- Drops the raw staging table once the clean table is created

## Next Steps

- Exploratory analysis of the cleaned `journeys` table (usage by station, time of day, seasonality, bike type)

## Project Files

- `load_data.py` ingests raw CSV files into PostgreSQL
- `transform.sql` transforms raw journey data into a clean, typed table

#### Local files needed
- `Data/` folder for the raw monthly CSV exports from [TfL Open Data](https://cycling.data.tfl.gov.uk/#!usage-stats%2F) between June 2025 and May 2026
- `.env` file containing:
    ```
    # Database Settings
    DB_PASSWORD=••••• # your PostgreSQL superuser password (account is called postgres by default)
    DB_PORT=XXXX # the PostgreSQL port (default is 5432)
    ```

## Dependencies

- Python, with the following libraries: `pandas`, `sqlalchemy`, `python-dotenv`, `psycopg2-binary`
    Install Python dependencies with:
    ```
    pip install pandas sqlalchemy python-dotenv psycopg2-binary
    ```
    (This might need to be prefixed with `python -m` if you are on windows)
- PostgreSQL (version 18)
    Again, make sure to put your port and superuser password in a `.env` file as explained above.

