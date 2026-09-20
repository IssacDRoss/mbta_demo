# Summary
Included in this repo are a few functions to interact with and query the MBTA api for information on the T train lines. The various questions achieved are described at the bottom of this readme, though the structure of the folder is meant more to be broadly applicable.


## Folder structure & contents

```
MBTA_DEMO 
├── routes.py               # Class for holding and interacting with a route
├── API_interfaces.py       # Methods that directly interact with the MBTA API
├── 1_list_subways.py       # Solution to 1st takehome question, prints list of each subway line
├── 2_enumerate_subways.py  # Solution to 2nd takehome question, prints 
|                             longest/shortest subway, and all transfer stations
├── 3_get_directions.py     # Solution to 3rd takehome question, prints *a* viable path between
|                             two provided stations
└── README.md               # Documentation of folder (i.e this very file)
```

# Take-home Questions
### Question 1
Write a problem that retrieves data representing what weʼll call “subway” routes:
“Light Rail” and “Heavy Rail” (types 0 and 1 in the API, respectively). The program
should print their names to the console.
A partial example of output:
Red Line, Blue Line, Orange Line, ...
There are two ways to filter results for subway-only routes:
 Download all data from the API ( https://api-v3.mbta.com/routes )and filter locally
on your computer
 Filter data with the API ( https://api-v3.mbta.com/routes?filter[type]=0,1 ) and
download just the filtered data to your computer
Please document your decision and your reasons for it.

#### Solution discussion
1. Download or Request? - I landed at requesting every time I run. the API key provides plenty of requests per minute, and a broadly more likely use case for something touching the mbta api is that it should have access to live information. Though the actual extent of these problems is extremely static, just manipulating a singular JSON download snapshot feels less relevant than leveraging the API's functionality for initial download. Certainly could justify downloading async for something deployed so it need not have an API key though.
2. I made a network class so as to contain the json output from a given request, methods for interacting with it, and simplify access to the data. Leaned into methods for the given questions being added to the class rather than constructing logic in the script that is actually run, as in theory you want to use and extend the methodology to other consumers or uses without duplication.


### Question 2
Extend your program so it displays additional information:
 The name of the subway route with the most stops and the count of its stops
 The name of the subway route with the fewest stops and the count of its stopsSoftware Engineer Take-Home Challenge2
 A list of the stops that connect two or more subway routes and the route
names for each of those stops

#### Solution discussion
1. This problem shows the weakness of just querying the API every time you want to know something (i.e. leveraging the stops endpoint per route)
2. Landed at polling all relevant stops per route during init, and having a getter to grab stops by line for later queries. This also led me to have a MBTARoute class to dramatically simplify the accessors for the types of information I actually want out of a given entry
3. the "include" arg enables a cross compilation of data, but its unwieldy for a lightweight query. Realistically the larger dataclass construction leveraging these would be good to use when you need a variety of interlinked info.



### Question 3
Extend your program again so the user can provide any two stops along the
subway routes you listed for question 1.
The program should list a rail route you could travel from one stop to the other. We
arenʼt evaluating your solution on the efficiency or cleverness of your route-
finding mechanism. Pick a simple solution that answers the question. We will want
you to understand and be able to explain how your algorithm performs.
Some examples:
 Davis to Kendall → Red Line
 Ashmont to Arlington → Red Line, Green Line
How you handle input, represent train routes, and present output is your choice.

#### Solutions discussion
1. handling input: took these as keyword --args to enforce that they are provided. Inspect the station names against the list of stations in network and list those stations if the user enters an unexpected station name. basic protection like case tolerance helps make this usable.
2. Train routes are a lot simpler to handle as a class than as an entry in a big json table of ~80% worthless info
3. Simple printing of what the user selected, what routes/stops they start->transfer->get off at is baked into the find_path method of the "network" class so this could in theory be leveraged as part of a larger whole
4. Algorithim for finding a path - while we could blindly traverse a map, a breadth-first search will be pretty simple and give us a short route, as opposed to potentially landing on some crazy circuitous route.
5. A couple of things emerge from wanting a map to traverse.
    A. well the stops can't just be a list of names anymore, they need to be actually structured along a direction of travel of the route. This necessitated additional sorting / processing on the MBTARoute object so it has an array that is traversable representing actually riding the train as opposed to alphabetically