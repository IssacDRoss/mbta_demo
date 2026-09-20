import API_interfaces
from network import MBTANetwork
import argparse

def main():
    parser = argparse.ArgumentParser(description="A script that accepts an API key.")
    parser.add_argument("--key", type=str, required=False, help="API key for MBTA API access. Optional, can run with no API key, and will look for system env variable MBTA_API_KEY if not provided.")
    # Parse the arguments
    args = parser.parse_args()

    # Check if a key argument was actually passed, use it if so
    if args.key:
        API_interfaces.set_mbta_api_key(args.key)

    # List the subway lines (heavy & light rail)
    
    # create a Routes object with a filter for subway lines (type=0 for subway & type=1 for light rail)
    params = {
        "filter[type]": "0,1",  # Filter for subway and light rail
        }
    subways = MBTANetwork(params=params)
    # print the names of all resultant lines
    print(f"Subway Lines: {subways.route_names}")

if __name__ == "__main__":
    main()