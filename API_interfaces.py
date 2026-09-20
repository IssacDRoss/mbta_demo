import os
import requests

# Baseline API url
BASE_API_URL = "https://api-v3.mbta.com"

def get_mbta_api_key():
    """
    Returns the MBTA API key from the environment variable.
    """    
    # Note, set a local environment variable called MBTA_API_KEY to your personal MBTA API key. (Sorry no free rides on public transit!)
    # You can request one here: https://api-v3.mbta.com/docs/swagger/index.html
    key = os.environ.get("MBTA_API_KEY")
    return key

def get_req(endpoint,args=None):
    """
    Returns the response from a GET request to the given endpoint and any additional arguments.
    """
    # if we have an API key available in the env vars, use it as another arg
    if get_mbta_api_key():
        args = f"{args}?api_key={get_mbta_api_key()}"
    resp = requests.get(f"{BASE_API_URL}/{endpoint}{args if args else ''}")
    return resp.json()

def get_all_lines():
    """
    Returns a list of all MBTA lines.
    Broadly useful for inspecting the json structure, if a bit cumbersome given the ~180 lines
    """
    resp = get_req("routes")
    return resp

def get_lines_filtered(**kwargs):
    """
    Returns a list of MBTA lines according to comma separated kwarg filters.
    Useful for filtering by type, mode, etc. See https://api-v3.mbta.com/docs/swagger/index.html#/Routes/get_routes for details.
    """
    # pile together the query parameters from the kwargs
    query_params = "&".join([f"{key}={value}" for key, value in kwargs.items()])
    # send request using routes url + api key + query parameters
    resp = get_req("routes", args=f"&{query_params}")
    return resp