# Summary
Included in this repo are a few functions to interact with and query the MBTA api for information on the T train lines. The various questions achieved are described at the bottom of this readme, though the structure of the folder is meant more to be broadly applicable.


## Folder structure & contents

```
MBTA_DEMO 
├── routes.py               # Class for holding and interacting with a route
├── API_interfaces.py       # Methods that directly interface with the MBTA API
├── 1_list_subways.py       # Solution to 1st takehome question, prints list of each subway line
├── 2_enumerate_subways.py  # Solution to 2nd takehome question, prints 
|                             longest/shortest subway, and all transfer stations
├── 3_get_directions.py     # Solution to 3rd takehome question, prints *a* viable path between
|                             two provided stations
└── README.md               # Documentation of folder (i.e this very file)
```

## Running / Testing
I decided to split the 3 problems into their own little scripts that can be run via:
1. `python 1_list_subways.py`
2. `python 2_enumerate_subways.py`
3. `python 3_get_directions.py --start "YOUR FAVORITE STATION" --end "SOME COOL DESTINATION"`
Definitely produces some cruft with regard to adding the argparser for passing the key each time, but I didn't feel that a little gui or argument for which problem felt necessary. Obviously actually using this MBTANetwork class practically would have cleaner entrants, but this shows the ease of construction and advantage of putting most repeatable functionality as methods to that class.

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
2. I made a Network class so as to contain the json output from a given response of the /Routes request, methods for interacting with it, and simplify access to the data. Leaned into methods for the given questions being added to the class rather than constructing logic in the script that is actually run, as in theory you want to use and extend the methodology to other consumers or uses without duplication.


### Question 2
Extend your program so it displays additional information:
 The name of the subway route with the most stops and the count of its stops
 The name of the subway route with the fewest stops and the count of its stopsSoftware Engineer Take-Home Challenge2
 A list of the stops that connect two or more subway routes and the route
names for each of those stops

#### Solution discussion
1. This problem shows the weakness of just querying the API every time you want to know something (i.e. leveraging the /Stops endpoint per route)
2. Landed at polling all relevant stops per route during init, and having a getter to grab stops by line for later queries. This also led me to have a MBTARoute class to dramatically simplify the accessors for the types of information I actually want out of a given route entry. Considered the same for stops so I could more cleanly construct the transfer station concept, but felt there weren't enough methods or properties we'd want so i just stuck with handling the json output more directly.
3. the "include" arg enables a cross coordination of data, such as which stops belong to which routes, but its unwieldy. Realistically the larger dataclass construction leveraging these would be good to use when you need a variety of interlinked info.



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
1. handling input: took these as keyword --args to enforce that they are provided. Inspect the station names against the list of stations in network and list those stations if the user enters an unexpected station name. basic protection like case tolerance and partial matching helps make this more usable.
2. Algorithim for finding a path: We could theoretically blindly traverse routes and expect this to fall within 3 transfers given the structure of the subway routes. That's of course short sighted if we ever want to includ busses or otherwise be adaptive. A breadth-first search will be pretty simple and gives us a short route (at least in terms of # of stops), without having to weight off of travel times or # of transfers taken. Would I like if that's how the transit app worked? probably not, but this would get ya there!
3. There's a pretty clear weakness in the method when you look along the green line. we pick literally the first entry that gets us down a path, and often times that can mean first getting on green line D until you reach the fork then hopping on the relevant green line B that actually goes to your end destination.
4. Probably really want to use A* so we can have weights against transfers, and only pursue directions that actually move us in the direction of travel