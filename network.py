import API_interfaces
from route import MBTARoute
from collections import defaultdict, deque

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
        Returns a list of route names and stops connecting start_stop to end_stop using Breadth-First Search on self.graph built above.
        """

        # protect against inexact / incorrect entry
        start_id, start_name = self.handle_stop_names(start_stop)
        end_id, end_name = self.handle_stop_names(end_stop)

        print(f"Finding path between two stops in the MBTA subway network.")
        print(f"Start stop: {start_name}, End stop: {end_name}")

        # Queue items: (current_stop_id, path)
        # path entry format: (from_stop_id, to_stop_id, route_used)
        queue = deque([(start_id, [])])
        visited = {start_id}

        # keep exploring for as long as we can keep adding new stops to the search queue
        while queue:
            # pop the current location off the top of the search queue
            current_stop, path = queue.popleft()

            # check for completion of path
            if current_stop == end_id:
                # print out a nicely formatted set of instructions
                return self._format_route_path(path)

            # for every neighboring station, along each route, of the current stop
            for neighbor_id, routes in self.graph[current_stop].items():
                # skip already visited stops (i.e. don't make a loop)
                if neighbor_id not in visited:
                    visited.add(neighbor_id)
                    # Select the first line connecting these two adjacent stops
                    route_used = next(iter(routes))
                    # track the path taken to reach this new station
                    new_path = path + [(current_stop, neighbor_id, route_used)]
                    # add to search queue
                    queue.append((neighbor_id, new_path))

        print(f"No path found after performing search of network!")
        return []

    def _format_route_path(self, path):
        """Compresses step-by-step station edges into an ordered list of lines taken and transfer stations used, then print that out legibly."""
        lines_used = []
        transfers = []
        for to_id, fro_id, route_id in path:
            if not lines_used or lines_used[-1] != self.routes[route_id].route_name:
                lines_used.append(self.routes[route_id].route_name)
                transfers.append(self.in_network_stops[fro_id]['attributes']['name'])

        # Produce i nice human readable set of directions
        print(f"Route Found! Embark the {lines_used[0]} at {self.in_network_stops[path[0][1]]['attributes']['name']}.")
        # list each transfer taken (i.e. only between trains)
        for i in range(1,len(lines_used)):
            print(f"Transfer to the {lines_used[i]} at {transfers[i]}")
        print(f"Disembark the {lines_used[-1]} at {self.in_network_stops[path[-1][0]]['attributes']['name']}. You have arrived!")

        return lines_used, transfers


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

        # return just the one value, the list was only relevant for searching for multiple matches
        return stop_id[0], stop_name[0]


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
