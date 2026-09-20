# Summary
Included in this repo are a few functions to interact with and query the MBTA api for information on the T train lines. The various questions achieved are described at the bottom of this readme, though the structure of the folder is meant more to be broadly applicable.


## Folder structure & contents

```
MBTA_DEMO 
├── routes.py             # Class for holding and interacting with a route
├── API_interfaces.py     # Methods that directly interact with the MBTA API
├── solutions.py          # "Solutions" to each takehome question, 
|                           i.e. runnable functions to address each task
└── README.md             # Documentation of folder (i.e this very file)
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
1. Download or Request? - I landed at requesting every time I run. the API key provides plenty of requests per minute, and a broadly more likely use case for something touching the mbta api is that it should have access to live information. Though the actual extent of these problems is extremely static, just manipulating the singular JSON download snapshot feels less relevant than leveraging the API's functionality. Certainly could justify downloading async for something deployed so it need not have an API key though.


### Question 2
Extend your program so it displays additional information:
 The name of the subway route with the most stops and the count of its stops
 The name of the subway route with the fewest stops and the count of its stopsSoftware Engineer Take-Home Challenge2
 A list of the stops that connect two or more subway routes and the route
names for each of those stops



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