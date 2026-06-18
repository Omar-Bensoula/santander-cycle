import os
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine

file_names = os.listdir("Data")

load_dotenv()
engine = create_engine(f'postgresql://postgres:{os.getenv("DB_PASSWORD")}@localhost:{os.getenv("DB_PORT")}/santander_cycles')

for i, file_name in enumerate(file_names):

    df = pd.read_csv(f"Data/{file_name}")

    print(f"Loading {i+1}/{len(file_names)}")

    df.rename(columns={
        "Number": "number_id",
        "Start date": "start_date",
        "Start station number": "start_station_number",
        "Start station": "start_station",
        "End date": "end_date",
        "End station number": "end_station_number",
        "End station": "end_station",
        "Bike number": "bike_number",
        "Bike model": "bike_model",
        "Total duration": "total_duration",
        "Total duration (ms)": "total_duration_ms"
    }, inplace=True)

    df.to_sql("journeys_raw", engine, if_exists="append", index=False)

print("Done")
