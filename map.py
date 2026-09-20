from collections import deque
from network import MBTANetwork

DEBUG = False

class MBTAMap:
    """
    Class for generating a map of a given MBTA network, including functionality for finding paths between stops.
    """
    def __init__(self, network: MBTANetwork):
        """
        Initializes the MBTANetwork class given an initialized MBTANetwork.
        """
        self.network = network
        self.graph = self._build_graph()

    def _build_graph():
        """Generate a graph from the stops of the network as nodes, and routes as the edges between nodes"""

        # Constructing this stop-first as opposed to generating a tree based on the routes.



    def find_path(self, start_stop, end_stop):
                """
                Returns a list of routes that connect the start and end stops.
                """
                # check if the start and end stops are in the network
                if start_stop not in self.in_network_stops:
                    raise ValueError(f"Start stop {start_stop} is not in the network.")
                if end_stop not in self.in_network_stops:
                    raise ValueError(f"End stop {end_stop} is not in the network.")
        
                print(f"Finding path between two stops in the MBTA subway network.")
                print(f"Start stop: {start_stop}, End stop: {end_stop}")
                # naive check for direct connections, i.e. if both stops are on the same route
                connecting_routes = []
                for route in self.routes:
                    if start_stop in route.stops and end_stop in route.stops:
                        print(f"Direct connection found on route {route.route_name}.")
                        connecting_routes.append(route.route_name)
                        return connecting_routes
        
                # if no direct connection, check for transfer stations on the lines
                
                
                return connecting_routes