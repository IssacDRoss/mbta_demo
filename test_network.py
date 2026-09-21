import unittest
from unittest.mock import patch, MagicMock
from network import MBTANetwork

class TestMBTANetwork(unittest.TestCase):

    def setUp(self):
        """Set up mock data and patch API call before each test."""
        # Define mock stops for Red Line (3 stops)
        self.red_stops = [
            {"id": "stop-alewife", "attributes": {"name": "Alewife"}},
            {"id": "stop-davis", "attributes": {"name": "Davis"}},
            {"id": "stop-park", "attributes": {"name": "Park Street"}}
        ]

        # Define mock stops for Green-B Line (2 stops, overlapping at Park Street)
        self.green_stops = [
            {"id": "stop-park", "attributes": {"name": "Park Street"}},
            {"id": "stop-boylston", "attributes": {"name": "Boylston"}}
        ]

        # Mock JSON return from API_interfaces.get_routes_filtered
        self.mock_api_return = {
            "data": [
                {"id": "Red", "attributes": {"long_name": "Red Line"}},
                {"id": "Green-B", "attributes": {"long_name": "Green Line B"}}
            ]
        }

    @patch("network.API_interfaces.get_routes_filtered")
    @patch("network.MBTARoute")
    def test_initialization_and_enumeration(self, mock_mbta_route_cls, mock_get_routes):
        """Test that network initializes routes, stops, and transfer stations correctly."""
        mock_get_routes.return_value = self.mock_api_return

        # Configure MBTARoute mock instances returned during __init__ loop
        mock_red = MagicMock()
        mock_red.route_name = "Red Line"
        mock_red.stops = self.red_stops

        mock_green = MagicMock()
        mock_green.route_name = "Green Line B"
        mock_green.stops = self.green_stops

        mock_mbta_route_cls.side_effect = [mock_red, mock_green]

        network = MBTANetwork()

        # 1. Verify routes dict
        self.assertEqual(len(network.routes), 2)
        self.assertIn("Red", network.routes)
        self.assertIn("Green-B", network.routes)

        # 2. Verify unique stops identified
        self.assertEqual(len(network.in_network_stops), 4)

        # 3. Verify Park Street identified as transfer station (connects Red & Green-B)
        self.assertIn("stop-park", network.transfer_stations)
        self.assertCountEqual(
            network.transfer_stations["stop-park"]["connections"], 
            ["Red", "Green-B"]
        )

    @patch("network.API_interfaces.get_routes_filtered")
    @patch("network.MBTARoute")
    def test_get_longest_and_shortest_route(self, mock_mbta_route_cls, mock_get_routes):
        """Test route length comparisons."""
        mock_get_routes.return_value = self.mock_api_return

        mock_red = MagicMock()
        mock_red.route_name = "Red Line"
        mock_red.stops = self.red_stops  # 3 stops

        mock_green = MagicMock()
        mock_green.route_name = "Green Line B"
        mock_green.stops = self.green_stops  # 2 stops

        mock_mbta_route_cls.side_effect = [mock_red, mock_green]

        network = MBTANetwork()

        name, length = network.get_longest_route()
        self.assertEqual(name, "Red Line")
        self.assertEqual(length, 3)

        name, length = network.get_shortest_route()
        self.assertEqual(name, "Green Line B")
        self.assertEqual(length, 2)

    @patch("network.API_interfaces.get_routes_filtered")
    @patch("network.MBTARoute")
    def test_graph_construction(self, mock_mbta_route_cls, mock_get_routes):
        """Test that adjacency graph correctly connects adjacent stations."""
        mock_get_routes.return_value = self.mock_api_return

        mock_red = MagicMock(route_name="Red Line", stops=self.red_stops)
        mock_green = MagicMock(route_name="Green Line B", stops=self.green_stops)
        mock_mbta_route_cls.side_effect = [mock_red, mock_green]

        network = MBTANetwork()

        # Verify bidirectional adjacency between Alewife and Davis
        self.assertIn("Red", network.graph["stop-alewife"]["stop-davis"])
        self.assertIn("Red", network.graph["stop-davis"]["stop-alewife"])

        # Verify Park Street links both Red Line to Davis AND Green Line to Boylston
        self.assertIn("Red", network.graph["stop-park"]["stop-davis"])
        self.assertIn("Green-B", network.graph["stop-park"]["stop-boylston"])

    @patch("network.API_interfaces.get_routes_filtered")
    @patch("network.MBTARoute")
    def test_find_path_valid_transfer(self, mock_mbta_route_cls, mock_get_routes):
        """Test pathfinding between two stops requiring a line transfer (Alewife to Boylston)."""
        mock_get_routes.return_value = self.mock_api_return

        mock_red = MagicMock(route_name="Red Line", stops=self.red_stops)
        mock_green = MagicMock(route_name="Green Line B", stops=self.green_stops)
        mock_mbta_route_cls.side_effect = [mock_red, mock_green]

        network = MBTANetwork()

        lines_used, transfers = network.find_path("Alewife", "Boylston")
        # Should take Red Line to Park Street, then transfer to Green Line B at Park Street
        self.assertEqual(lines_used, ["Red Line", "Green Line B"])
        self.assertEqual(transfers, ["Alewife", "Park Street"])

    @patch("network.API_interfaces.get_routes_filtered")
    @patch("network.MBTARoute")
    def test_find_path_invalid_stop_raises_error(self, mock_mbta_route_cls, mock_get_routes):
        """Test that passing a non-existent stop raises a ValueError."""
        mock_get_routes.return_value = self.mock_api_return
        mock_mbta_route_cls.side_effect = [
            MagicMock(route_name="Red Line", stops=self.red_stops),
            MagicMock(route_name="Green Line B", stops=self.green_stops)
        ]

        network = MBTANetwork()

        with self.assertRaises(ValueError):
            network.find_path("Fake Station", "Boylston")


if __name__ == "__main__":
    unittest.main()