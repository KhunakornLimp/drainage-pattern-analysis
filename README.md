# drainage-pattern-analysis

My mini project for the Year 1 Programming for Geoscientists module.

### Assignment

Basic functionality: You are provided with a ‘DTM’ file dtm50.txt, which represents digital terrain model data (heights) at 50m intervals over a 10km x 10km square of hilly terrain in Scotland. The values are space-separated (not comma separated), and are in logical order (so the each row is 200 heights above sea level, in meters, from west to east, and rows are arranged from north to south. The data is visualised on the right as a greyscale image, where white is high and dark is low. Write a program that treats this area as a 200 x 200 grid of squares, each with a height obtained from the DTM data, and uses this to analyse which squares are likely to experience relatively high and relatively low waterflow. Use a simple waterflow model, where rainfall is evenly distributed across the area, and water always moves from one square to the lowest adjacent square (so always moves North, South, East or West). To simulate what happens to rain falling on any particular square, determine its path by repeatedly tracking its movement downhill, until it moves into a square on the edge of the grid (where you cannot calculate flow direction properly). If there are two equally low possible directions, your simulation should choose one at random. Your simulation will also need to make sure that the path cannot visit the same square twice, or find some other way to make sure that it cannot get into a ‘loop’. Your program will need to keep track of how many of these ‘water paths’ pass through each square to assess its relative waterflow.
Your program’s output should be a 200x200 pixel image file, in which areas of high flow are brighter than those of low flow. 
Note that this is genuine real-world data – and our model is simple. This means that results might not look ‘perfect’. One issue is that this dataset actually includes a lake, which may or may not become obvious as you look at the output. One thing that HAS been fixed in this data though – there are no ‘sink points’, i.e. no squares which are lower than all surrounding.
Some ideas for harder things to try to add: The basic program is hard already! You could implement more complex models (e.g. movement is also allowed diagonally). You could try to automatically identify the lake, and deal with it in some clever way. I’ll leave you to come up with more…

### Feedback

Function: 23 It's probably the slowest version of this I've seen, but that's not a problem - I didn't ask for it to run fast. I suspect the slow bits are the complex comprehensions in lines 72-78 - these are clever and certainly do the job, but apparently not quickly. I suspect also that your approach to dealing with flat areas, which allows water to flow around randomly for a long while, is also a source of slowness. It does make the lake pop out nicely though! Anyway as far as I'm concerned this does precisely what I asked for, so full marks for function. 
Style: 7 Well commented and well explained at the start. Perhaps could be a little more spaced out - rather dense in places - but otherwise code style is good, and flake8 is certainly happy. There are many very clever things in the way you've built this (one example is the use of shape to detect edge-hits). To be ultra-critical, there is some inconsistency in variable naming ('ZFlow', 'surr_corr') and occasionally I felt variable names were more cryptic than they needed to be. Overall though I have no substantial issues with your style. 
Extras: 7 There are a lot! Your matplotlib output is very nice - the contours in particular are a superb touch, and the log scale helps too. Identifying the lake programmatically was great to see too. There is plenty of cunning use of python as well (dict. comps as you point out), and the animation was a nice final touch. In the end of course changing the absolute values input doesn't change the pattern (as it's still spread evenly over the map), but still was good to see. Perhaps you could have found a simple model for topographic influence on rainfall and used _that_ for more sophisticated inputs? Perhaps also you could have broken your code down a bit using functions? Overall though you've done loads here, and I'm really impressed. 
Overall: 37/40 This is truly superb - very high marks are meant to be extremely hard to get for this project, but this has ended up (deservedly) with a mark equivalent to over 90%. You are clearly very good indeed at both coding and at computational thinking, and have produced a really really good project that you should be very proud of.
