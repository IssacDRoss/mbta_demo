import API_interfaces
import argparse

# solution_1 - Get all subway lines of the MBTA and print them
def list_subway_lines():
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

    # List the subway lines (heavy & light rail)
    list_subway_lines()

if __name__ == "__main__":
    main()