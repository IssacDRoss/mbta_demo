import os
import requests

# Baseline API url
BASE_API_URL = "https://api-v3.mbta.com"

def get_mbta_api_key():
    """
    Returns the MBTA API key from the environment variable.
    """    
    # Note, set a local environment variable called MBTA_API_KEY to your personal MBTA API key. (Sorry only a few free rides on public transit!)
    # You can request one here: https://api-v3.mbta.com/docs/swagger/index.html
    key = os.environ.get("MBTA_API_KEY")
    return key

def get_default_header():
    """
    Returns a default header for the MBTA API request.
    """
    headers = {}

    # if we have an API key available in the env vars, use it as another arg
    if get_mbta_api_key():
        headers["X-API-Key"] = get_mbta_api_key()
    
    return headers

def set_mbta_api_key(key):
    """
    Sets the MBTA API key in the environment variable for this session
    Useful for just passing a key
    """
    os.environ["MBTA_API_KEY"] = key

def get_req(endpoint,params=None):
    """
    Returns the response from a GET request to the given endpoint and any additional arguments.
    """
    resp = requests.get(f"{BASE_API_URL}/{endpoint}", params=params, headers=get_default_header())
    return resp.json()

def get_all_lines():
    """
    Returns a list of all MBTA lines.
    Broadly useful for inspecting the json structure, if a bit cumbersome given the ~180 lines
    """
    resp = get_req("routes")
    return resp

def get_routes_filtered(params=None):
    """
    Returns a list of MBTA routes according to json filters.
    Useful for filtering by type, mode, etc. See https://api-v3.mbta.com/docs/swagger/index.html#/Routes/get_routes for details.
    """
    # send request using routes url + query parameters
    resp = get_req("routes", params=params)
    return resp

def get_stops_filtered(params={}):
    """
    Returns a list of MBTA stops according to json filters.
    Useful for filtering by type, mode, etc. See https://api-v3.mbta.com/docs/swagger/index.html#/Stops/get_stops for details.
    """
    # send request using stops url + query parameters
    resp = get_req("stops", params=params)
    return resp