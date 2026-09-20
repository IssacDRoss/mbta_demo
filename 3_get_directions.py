import API_interfaces
import argparse
from network import MBTANetwork
from map import MBTAMap

def main():
    parser = argparse.ArgumentParser(description="A script that accepts an API key.")
    parser.add_argument("--key", type=str, required=False, help="API key for MBTA API access. Optional, can run with no API key, and will look for system env variable MBTA_API_KEY if not provided.")
    parser.add_argument("--start", type=str, required=True, help="Start stop for the path.")
    parser.add_argument("--end", type=str, required=True, help="End stop for the path.")
    # Parse the arguments
    args = parser.parse_args()

    # Check if a key argument was actually passed, use it if so
    if args.key:
        API_interfaces.set_mbta_api_key(args.key)

    params = {
            "filter[type]": "0,1",   # Filter for subway and light rail
            }
    subways = MBTANetwork(params=params)
    map = MBTAMap(subways)
    map.find_path(args.start, args.end)


if __name__ == "__main__":
    main()