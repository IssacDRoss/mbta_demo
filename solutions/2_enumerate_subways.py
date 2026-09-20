import API_interfaces
import argparse

def find_longest_subway():
    # retrieve and print all "subway" lines of the MBTA
    # type=0 for subway & type=1 for light rail.
    lines = API_interfaces.get_lines_filtered(type=[0,1])
    names = [line['attributes']['long_name'] for line in lines['data']]

    print(names)

    return 

def main():
    parser = argparse.ArgumentParser(description="A script that accepts an API key.")
    parser.add_argument("--key", type=str, required=False, help="API key for MBTA API access. Optional, can run with no API key, and will look for system env variable MBTA_API_KEY if not provided.")
    # Parse the arguments
    args = parser.parse_args()

    # Check if a key argument was actually passed, use it if so
    if args.key:
        API_interfaces.set_mbta_api_key(args.key)

    # Find the name of the longest subway and all how long it is
    find_longest_subway()
    # Same for the shortest subway
    find_shortest_subway()
    # List all stops that connect 2 or more routes, i.e. transfer stations
    list_transfer_stations()


if __name__ == "__main__":
    main()