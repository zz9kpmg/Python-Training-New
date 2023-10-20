import numpy as np
import pandas as pd
import requests
import zipfile
import io
import sqlite3
import configs
from google.transit import gtfs_realtime_pb2
import json


def download_timetable_data():
    headers = {
        "Accept": "application/octet-stream",
        "Authorization": "apikey " + configs.api_key_1,
    }

    response = requests.get(
        "https://api.transport.nsw.gov.au/v1/publictransport/timetables/complete/gtfs",
        headers=headers,
        stream=True,
        verify=r"C:\Users\zzhang9\OneDrive - KPMG\Documents\Python\Advanced Course Project\caadmin.netskope.com",
    )

    z = zipfile.ZipFile(io.BytesIO(response.content))
    z.extractall(
        r"C:\Users\zzhang9\OneDrive - KPMG\Documents\Python\Advanced Course Project\Data\Timetable"
    )

    del response


def download_position_data():
    headers = {
        "Accept": "application/x-google-protobuf",
        "Authorization": "apikey " + configs.api_key_1,
    }

    feed = gtfs_realtime_pb2.FeedMessage()

    response = requests.get(
        "https://api.transport.nsw.gov.au/v1/gtfs/vehiclepos/buses",
        headers=headers,
        stream=True,
        verify=r"C:\Users\zzhang9\OneDrive - KPMG\Documents\Python\Advanced Course Project\caadmin.netskope.com",
    )

    feed.ParseFromString(response.content)
    print("There are {} buses in the dataset.".format(len(feed.entity)))
    # bus = feed.entity[0:2]
    # print(bus)

    df = pd.DataFrame(
        columns=[
            "trip_id",
            "route_id",
            "start_time",
            "start_date",
            "schedule_relationship",
            "vehicle_id",
            "label",
            "license_plate",
            "latitude",
            "longitude",
            "bearing",
            "speed",
            "timestamp",
            "congestion_level",
            "occupancy_status",
        ]
    )

    for entity in feed.entity:
        entity_dict = {
            "trip_id": [entity.vehicle.trip.trip_id],
            "route_id": [entity.vehicle.trip.route_id],
            "start_time": [entity.vehicle.trip.start_time],
            "start_date": [entity.vehicle.trip.start_date],
            "schedule_relationship": [entity.vehicle.trip.schedule_relationship],
            "vehicle_id": [entity.vehicle.vehicle.id],
            "label": [entity.vehicle.vehicle.label],
            "license_plate": [entity.vehicle.vehicle.license_plate],
            "latitude": [entity.vehicle.position.latitude],
            "longitude": [entity.vehicle.position.longitude],
            "bearing": [entity.vehicle.position.bearing],
            "speed": [entity.vehicle.position.speed],
            "timestamp": [entity.vehicle.timestamp],
            "congestion_level": [entity.vehicle.congestion_level],
            "occupancy_status": [entity.vehicle.occupancy_status],
        }
        entity_df = pd.DataFrame.from_dict(entity_dict)
        df = pd.concat([df, entity_df], ignore_index=True)
    return df


def save_to_sql(connection, name):
    data_stops = pd.read_csv("Data\\Timetable\\stops.txt", sep=",")
    data_stops.to_sql(name, connection, if_exists="replace")
    print(connection.total_changes)


def list_sql_tables(connection):
    cursor = connection.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    print(cursor.fetchall())


def read_from_sql(connection, name):
    return pd.read_sql_query("SELECT * FROM " + name, connection)


if __name__ == "__main__":
    # download_timetable_data()
    connection = sqlite3.connect("transport.db")
    # save_to_sql(connection)
    # list_sql_tables(connection)
    # read_from_sql(connection)

    position_df = download_position_data()
    print(position_df.head())

    position_df.to_sql('bus_positions', connection, if_exists="replace")
    list_sql_tables(connection)

    position_df_read = read_from_sql(connection, 'bus_positions')
    print(position_df_read.head())
