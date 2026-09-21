import API_interfaces
from route import MBTARoute
from collections import defaultdict

DEBUG = True

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
        self.routes = {}
        for route in self.json_return['data']:
            self.routes[route['id']] = MBTARoute(route)

        self._enumerate_stops()
        self._build_graph()

    # Methods for various interesting queries
    def get_longest_route(self):
        """
        Returns the longest route in the list of MBTA routes.
        """
        longest_route = max(
            self.routes, 
            key=lambda route: len(self.routes[route].stops))

        route_name = self.routes[longest_route].route_name
        length = len(self.routes[longest_route].stops)
        print(f"Longest Subway: {route_name}, number of stops = {length}")
        return route_name, length

    def get_shortest_route(self):
        """
        Returns the shortest route in the list of MBTA routes.
        """
        shortest_route = min(
            self.routes, 
            key=lambda route: len(self.routes[route].stops))

        route_name = self.routes[shortest_route].route_name
        length = len(self.routes[shortest_route].stops)
        print(f"shortest Subway: {route_name}, number of stops = {length}")
        return route_name, length

    def list_transfer_stations(self):
        """
        Prints a readable list of transfer stations in the network, including the routes that connect at each station.
        """
        for tf in self.transfer_stations:
            # find all routes that connect at this transfer station
            print(f"Transfer Station - {self.transfer_stations[tf]['name']}, connects routes: {self.transfer_stations[tf]['connections']}")

    def _enumerate_stops(self):
        """
        Determines list stops for all routes in the network of MBTA routes.
        Useful for rejecting impossible routes, e.g. if a stop is not in the list of stops for any route "in network", it is not a valid stop.

        Also determines if a stop is a "transfer station" 
        A transfer station is defined as a stop that connects 2 or more routes, specifically that are within the network / filter this class contains.
        """
        stops = {}
        for route_id, route in self.routes.items():
            for cur_stop in route.stops:
                id = cur_stop['id']
                # add only unique stops to the list
                if id not in stops:
                    stops[id] = cur_stop
                    stops[id]['connecting_routes'] = []
                # add any routes (i.e. possible multiple) to set of connections
                stops[id]['connecting_routes'].append(route_id)

        self.in_network_stops = stops
        self.transfer_stations = {}

        for stop_id, cur_stop in self.in_network_stops.items():
            if len(cur_stop['connecting_routes']) > 1:
                self.transfer_stations[stop_id] = {
                    'connections': cur_stop['connecting_routes'],
                    'name': cur_stop['attributes']['name']
                }

    def _build_graph(self):
        """Generate a graph from the stops of the network as nodes, and routes as the edges between nodes"""

        # Constructing this stop-first as opposed to generating a tree based on the routes. structure is from each graph, what are it's neighbors, and upon what line to you travel to get to that neighbor?
        # e.g. graph[x][y] = set of route_ids connecting stop x to stop y
        self.graph = defaultdict(lambda: defaultdict(set))

        for route_id, route in self.routes.items():
            # Iterate sequentially through the stops array of the route (which is thankfully in order already)
            for i in range(len(route.stops) - 1):
                stop_x = route.stops[i]['id']
                stop_y = route.stops[i + 1]['id']

                # Add bi-directional edge between adjacent stations
                # we add an edge as opposed to just setting the element since they might be neighbors along multiple routes (e.g. green E & green D)
                self.graph[stop_x][stop_y].add(route_id)
                self.graph[stop_y][stop_x].add(route_id)

                # debug prints for ensuring the construction script is working
                if DEBUG:
                    print(f"added new neighbors {stop_x} connects to {stop_y} via {route.route_name}")


    def find_path(self, start_stop, end_stop):
        """
        Returns a list of routes that connect the start and end stops.
        """

        # protect against inexact / incorrect entry
        start_id, start_name = self.handle_stop_names(start_stop)
        end_id, end_name = self.handle_stop_names(end_stop)

        print(f"Finding path between two stops in the MBTA subway network.")
        print(f"Start stop: {start_name}, End stop: {end_name}")
        # naive check for direct connections, i.e. if both stops are on the same route
        connecting_routes = []
        for route_id, route in self.routes.items():
            if start_id in route.stops and end_id in route.stops:
                print(f"Direct connection found on route {route.route_name}.")
                connecting_routes.append(route.route_name)
                return connecting_routes

        # if no direct connection, check for transfer stations on the lines
        
        return connecting_routes

    def handle_stop_names(self, stop_name):
            """Protect around user entering a stop name that isn't obvious exactly a key. Return the id for stop, along with formatted name"""
            # convert to title case, which is the format stop names are stored with
            search_val = stop_name.title()
    
            stop_id = []
            stop_name = []
            # find the key / id for the given stop name within the in-network stops
            # specifically looking for partial matches
            for id, stop in self.in_network_stops.items():
                if search_val in stop['attributes']['name']:
                    stop_id.append(id)
                    stop_name.append(stop['attributes']['name'])
    
            if len(stop_id) < 1:
                print (self.stop_names)
                raise ValueError(f"Stop entry {search_val} is not in the network. See above list of stops we have in-network")
            if len(stop_id) > 1:
                raise ValueError(f"Stop entry ['{stop_name}'] is ambiguous, specify between {stop_name}")
    
            return stop_id, stop_name
    
    

    @property
    def route_names(self):
        """
        Returns a list of the long names (i.e. including 'line') of the MBTA routes.
        """
        return [route.route_name for route_id, route in self.routes.items()]

    @property
    def stop_names(self):
        """
        Returns a list of the long names stops in the network
        """
        return [stop['attributes']['name'] for stop_id, stop in self.in_network_stops.items()]
