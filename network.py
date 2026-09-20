import API_interfaces
from route import MBTARoute

DEBUG = False

class MBTANetwork:
    """
    Class for storing & interacting with a list or "network" of MBTA routes, providing methods for various filters or queries
    """
    def __init__(self, params=None):
        """
        Initializes the MBTARoutes class based on a provided set of filters.
        given no filters, will return all routes. Filters can be provided as kwargs, e.g. type=0 for subway, fare_class="Local Bus" for busses, etc.
        See https://api-v3.mbta.com/docs/swagger/index.html#/Routes/get_routes for details.
        """
        self.json_return = API_interfaces.get_routes_filtered(params=params)
        self.routes = []
        for route in self.json_return['data']:
            self.routes.append(MBTARoute(route))

        self.in_network_stops = self._get_in_network_stops()
        self.transfer_stations = self._get_transfer_stations()

    # Methods for various interesting queries
    def get_longest_route(self):
        """
        Returns the longest route in the list of MBTA routes.
        """
        longest_route = max(
            self.routes, 
            key=lambda route: len(route.stops))

        route_id = longest_route.route_id
        length = len(longest_route.stops)
        print(f"Longest Subway: {route_id}, number of stops = {length}")
        return route_id, length

    def get_shortest_route(self):
        """
        Returns the shortest route in the list of MBTA routes.
        """
        shortest_route = min(
            self.routes, 
            key=lambda route: len(route.stops))

        route_id = shortest_route.route_id
        length = len(shortest_route.stops)
        
        print(f"Shortest Subway: {route_id}, number of stops = {length}")
        return route_id, length

    def list_transfer_stations(self):
        """
        Prints a readable list of transfer stations in the network, including the routes that connect at each station.
        """
        for tf in self.transfer_stations:
            tf_name = tf['attributes']['name']
            # find all routes that connect at this transfer station
            connecting_routes = []
            for route in self.routes:
                if tf in route.stops:
                    connecting_routes.append(route.route_name)
            print(f"Transfer Station: {tf_name}, connects routes: {connecting_routes}")

    def _get_in_network_stops(self):
        """
        Returns a list of stops for all routes in the network of MBTA routes.
        Useful for rejecting impossible routes, e.g. if a stop is not in the list of stops for any route "in network", it is not a valid stop.
        """
        stops = []
        for route in self.routes:
            for stop in route.stops:
                # add only unique stops to the list
                if stop not in stops:
                    stops.append(stop)
        return stops

    def _get_transfer_stations(self):
            """
            Returns a list of transfer stations in the list of MBTA routes.
            A transfer station is defined as a stop that connects 2 or more routes, specifically that are within the network / filter this class contains.
            """
            transfer_stations = []
            for stop in self.in_network_stops:
                # find all routes that connect at this stop
                connecting_routes = []
                for route in self.routes:
                    if stop in route.stops:
                        connecting_routes.append(route.route_name)
                if len(connecting_routes) > 1:
                    transfer_stations.append(stop)
            return transfer_stations

    @property
    def route_names(self):
        """
        Returns a list of the long names (i.e. including 'line') of the MBTA routes.
        """
        return [route.route_name for route in self.routes]
