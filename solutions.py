import API_interfaces

# solution_1 - Get all subway lines of the MBTA and print them
def list_subway_lines():
    # retrieve and print all "subway" lines of the MBTA
    # type=0 for subway & type=1 for light rail.
    lines = API_interfaces.get_lines_filtered(type=[0,1]) 

    print(lines)

    return 


def main():
    list_subway_lines()