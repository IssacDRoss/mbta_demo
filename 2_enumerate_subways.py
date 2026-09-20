import API_interfaces
import argparse
from routes import MBTANetwork

def main():
    parser = argparse.ArgumentParser(description="A script that accepts an API key.")
    parser.add_argument("--key", type=str, required=False, help="API key for MBTA API access. Optional, can run with no API key, and will look for system env variable MBTA_API_KEY if not provided.")
    # Parse the arguments
    args = parser.parse_args()

    # Check if a key argument was actually passed, use it if so
    if args.key:
        API_interfaces.set_mbta_api_key(args.key)

    params = {
            "filter[type]": "0,1",   # Filter for subway and light rail
            "include": "stop",       # Include stops in the response
            }
    subways = MBTANetwork(params=params)

    # Find the name of the longest subway and how long it is
    longest_subway, longest_length = subways.get_longest_route()
    print(f"Longest Subway: {longest_subway}, number of stops = {longest_length}")
    # Same for the shortest subway
    shortest_subway, shortest_length = subways.get_shortest_route()
    print(f"Shortest Subway: {shortest_subway}, number of stops = {shortest_length}")
    # List all stops that connect 2 or more routes, i.e. transfer stations
    subways.list_transfer_stations()


if __name__ == "__main__":
    main()