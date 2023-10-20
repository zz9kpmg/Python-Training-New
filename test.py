import numpy as np
import pandas as pd
import unittest
from program import Routes


class TestRoute(unittest.TestCase):
    def test_join_stop_data(self):
        routes_df = pd.DataFrame(
            data={"route": ["a", "a", "a", "a", "b", "b"], "stops": [1, 2, 3, 4, 2, 4]}
        )
        routes = Routes(routes_df)
        stops_df = pd.DataFrame(
            data={
                "stops": [1, 2, 3, 4],
                "location": ["Eastwood", "Sydney", "Burwood", "Strathfield"],
            }
        )
        routes.join_stop_data(stops_df)
        expected_df = pd.DataFrame(
            data={
                "route": ["a", "a", "a", "a", "b", "b"],
                "stops": [1, 2, 3, 4, 2, 4],
                "location": [
                    "Eastwood",
                    "Sydney",
                    "Burwood",
                    "Strathfield",
                    "Sydney",
                    "Strathfield",
                ],
            }
        )
        self.assertEqual(
            routes == expected_df, True, "Joining function not performing correctly"
        )

    def test_stop_in_route(self):
        routes_df = pd.DataFrame(
            data={"route": ["a", "a", "a", "a", "b", "b"], "stops": [1, 2, 3, 4, 2, 4]}
        )
        routes = Routes(routes_df)
        self.assertEqual(routes.in_route("a", 2), True, "Stop within route not found")
        self.assertEqual(routes.in_route("b", 2), True, "Stop within route not found")
        self.assertEqual(
            routes.in_route("b", 1), False, "Stop not within route incorrectly linked"
        )
        # self.assertEqual(routes.in_route('b', 1), True, 'This should fail')

    def test_list_routes(self):
        routes_df = pd.DataFrame(
            data={"route": ["a", "a", "a", "a", "b", "b"], "stops": [1, 2, 3, 4, 2, 4]}
        )
        routes = Routes(routes_df)
        self.assertListEqual(
            routes.list_routes(2, 4),
            ["a", "b"],
            "Routes connecting two stops not correctly listed",
        )
        self.assertListEqual(
            routes.list_routes(4, 2),
            ["a", "b"],
            "Routes connecting two stops not correctly listed",
        )
        self.assertListEqual(
            routes.list_routes(4, 1),
            ["a"],
            "Routes connecting two stops not correctly listed",
        )
        self.assertListEqual(
            routes.list_routes(5, 2),
            [],
            "Routes connecting two stops not correctly listed",
        )


if __name__ == "__main__":
    unittest.main()
