import API_interfaces

DEBUG = False

class MBTARoute:
    """
    Class for storing & interacting with a single MBTA route, providing methods for various filters or queries
    """
    def __init__(self, route):
        """
        Initializes the MBTARoute class based on a provided route object.
        """
        self.route = route
        self.route_id = route['id']
        self.route_name = self.route['attributes']['long_name']
        self.stops = self._get_stops_for_route(self.route_id)
        self.transfer_stations = []

    def _get_stops_for_route(self, route_id):
            """
            Returns a list of stops for a given route id, in order as they are on the route.
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