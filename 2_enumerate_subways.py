import API_interfaces
import argparse
from network import MBTANetwork

def main():
    """
    Solution script for problem 2, wrapping the wrapping the various queries to the subway structure so as to be runnable on it's own.
    """

    parser = argparse.ArgumentParser(description="A script that accepts an API key.")
    parser.add_argument("--key", type=str, required=False, help="API key for MBTA API access. Optional, can run with no API key, and will look for system env variable MBTA_API_KEY if not provided.")
    # Parse the arguments
    args = parser.parse_args()

    # Check if a key argument was actually passed, use it if so
    if args.key:
        API_interfaces.set_mbta_api_key(args.key)

    params = {
            "filter[type]": "0,1",   # Filter for subway and light rail
            }
    subways = MBTANetwork(params=params)

    # Find the name of the longest subway and how long it is
    subways.get_longest_route()    
    # Same for the shortest subway
    subways.get_shortest_route()
    # List all stops that connect 2 or more routes, i.e. transfer stations
    subways.list_transfer_stations()


if __name__ == "__main__":
    main()