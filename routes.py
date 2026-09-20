import API_interfaces

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
        json_return = API_interfaces.get_routes_filtered(params=params)
        self.routes = json_return['data']

    # Methods for various interesting queries
    def get_longest_route(self):
        """
        Returns the longest route in the list of MBTA routes.
        """
        longest_route = max(
            self.routes, 
            key=lambda route: len(self.get_stops_for_route(route['id'])))

        route_id = longest_route['id']
        length = len(self.get_stops_for_route(route_id))
        return route_id, length

    def get_shortest_route(self):
        """
        Returns the shortest route in the list of MBTA routes.
        """
        shortest_route = min(
            self.routes, 
            key=lambda route_id: len(self.get_stops_for_route(route_id)))

        route_id = shortest_route['id']
        length = len(self.get_stops_for_route(route_id))
        return route_id, length

    def get_stops_for_route(self, route_id):
        """
        Returns a list of stops for a given route id.
        """
        filt = {
            "filter[route]": route_id
            }
        stops = API_interfaces.get_stops_filtered(params=filt)

        # debug prints listing the stops for a given route
        if DEBUG:
            print (f"Route: {route_id}, number of stops = {len(stops['data'])}")
            print (f"Stops: {[stop['attributes']['name'] for stop in stops['data']]}")

        return stops['data']

    @property
    def transfer_stations(self):
        """
        Returns a list of transfer stations in the list of MBTA routes.
        A transfer station is defined as a stop that connects 2 or more routes, specifically that are within the network / filter this class contains.
        """
        transfer_stations = []
        for route in self.routes:
            for stop in self.get_stops_for_route(route['id']):
                # only append unique stops to the list of transfer stations
                if stop not in transfer_stations:
                    transfer_stations.append(stop)
        return transfer_stations

    @property
    def in_network_stops(self):
        """
        Returns a list of stops for all routes in the network of MBTA routes.
        Useful for rejecting impossible routes, e.g. if a stop is not in the list of stops for any route "in network", it is not a valid stop.
        """
        stops = []
        for route in self.routes:
            for stop in route['relationships']['stops']['data']:
                # add only unique stops to the list
                if stop not in stops:
                    stops.append(stop)
        return stops

    @property
    def route_names(self):
        """
        Returns a list of the long names (i.e. including 'line') of the MBTA routes.
        """
        return [route['attributes']['long_name'] for route in self.routes['data']]
