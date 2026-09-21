import API_interfaces
import argparse
from network import MBTANetwork

def main():
    """
    Solution script for problem 3, wrapping the wrapping construction and query of the subway network for the shortest route (by # of stops) between the provided stops. Takes stops by name (somewhat flexibly), prints a set of transfers one could take between those stops.
    """
    parser = argparse.ArgumentParser(description="A script that accepts an API key.")
    parser.add_argument("--key", type=str, required=False, help="API key for MBTA API access. Optional, can run with no API key, and will look for system env variable MBTA_API_KEY if not provided.")
    parser.add_argument("--start", type=str, required=True, help="Start stop name.")
    parser.add_argument("--end", type=str, required=True, help="Destination stop name.")
    # Parse the arguments
    args = parser.parse_args()

    # Check if a key argument was actually passed, use it if so
    if args.key:
        API_interfaces.set_mbta_api_key(args.key)

    params = {
            "filter[type]": "0,1",   # Filter for subway and light rail
            }
    subways = MBTANetwork(params=params)
    subways.find_path(args.start, args.end)


if __name__ == "__main__":
    main()