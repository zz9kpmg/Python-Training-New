import numpy as np
import pandas as pd


class Routes:
    """Dataframe with route information (route and stops) 
    and functions to determine stops in route."""

    # Initialise object
    def __init__(self, route_df):
        self.df = route_df

    # Joins stop data to route data by passing in a df with stops data.
    def join_stop_data(self, stops):
        return self

    # Checks if a stop is in a route
    def in_route(self, route, stop):
        """Checks a stop is within a route."""
        return (route + str(stop)) in (
            self.df["route"] + self.df["stops"].astype(str)
        ).unique()

    # Lists all routes connecting two stops.
    def list_routes(self, stop_start, stop_end):
        """Lists all routes connecting a starting and ending stop.
        Function is ambivalent to order of stops."""
        # Find all routes containing the starting stop
        df_routes_with_start = self.df[self.df["stops"] == stop_start]
        list_routes_with_start = df_routes_with_start["route"].unique().tolist()

        # Find all routes containing the ending stop
        df_routes_with_end = self.df[self.df["stops"] == stop_end]
        list_routes_with_end = df_routes_with_end["route"].unique().tolist()

        # List all routes with both stops and order in alphabetical order.
        list_routes_common = list(
            set(list_routes_with_start).intersection(list_routes_with_end)
        )
        list_routes_common.sort()
        return list_routes_common


class VehicleTrip:
    # Initialise object
    def __init__(self, trip_id, route, direction, arrival_time, departure_time):
        self.trip_id = trip_id
        self.route = route
        self.direction = direction
        self.arrival_time = arrival_time
        self.departure_time = departure_time

    def travel_time(self, stop_start, stop_end, route, time):
        pass


if __name__ == "__main__":
    print("Hello, World!")
    pass
    # Load stops data

    # Load routes data and add into Routes class

    # Join stops data to routes data
