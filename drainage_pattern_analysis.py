# drainage pattern analysis

'''
To begin with, all of the 200x200 grids in 10km x 10km area in Scotland are
dry, so their relative flow values are 0. Then, each grid is rained, and path
of water is determined by algorithm - water will move to lowest surrounding
grid (move randomly if there are 2 or more lowest ones), and it cannot move to
the grid which it has moved through (unless all the surrounding grids has been
moved through, so it will move randomly). The area has no sink, so the movement
of water will end at the edge of the area. The flow values of the grids which
are rained or flowed through will be +1 each time. By this algorithm, the
program runs raining on all the grids and accumulate flow values of each grid.
The cumulative flow values of each grid refer to its relative water flow, and
these will be visualised as a colourmap.

Extras including: 1. using stuff not taught in this course such as dictionary
comprehension and zip 2. allow water to flow diagonally 3. identify where the
lake is by assuming that it contains grid which has the maximum relative water
flow 4. add contours in the colourmap 5. create a log scale of relative water
flow 6. create animation showing monthly change of relative water flow from
October 2019 to September 2020
'''

# import required modules, needed to be installed first
import numpy as np
import matplotlib.pyplot as plt
import random2 as r
from matplotlib.colors import LogNorm

# read DTM50.txt file
height_file = open('C:/Users/Khuna/OneDrive - Imperial College London/ICL/Year 1/\
Programming for Geoscientists/Coursework/DTM50.txt', 'r')
# make list of 200 lists of 200 height values from each line
height_list = [row.strip().split(' ') for row in height_file.readlines()]
# change height_list to be 200x200 array
height_str = np.array(height_list)
# change all elements in the array from string to float
height_float = height_str.astype(np.float)
# make list from the float array
height_list = height_float.tolist()
# close the file
height_file.close()

# tell users to wait for animation and when they can close it
print('Please wait for an animation for few minutes.\n\
Please close the animation after the data of September 2020 have been shown \
for 2-3 seconds (due to bug in matplotlib and low speed of running).')

# make 200x200 array containing cumulative flow values, set all values 0 at
# initial (starting with no water flow in the area) for accumulating flow
# values from those by raining on each grid
cumulative_flow = np.zeros((200, 200))
#  make list of coordinates of all grids in the area
grid = [(X, Y) for X in range(200) for Y in range(200)]
# loop for finding array of flow value when raining on each grid
for g in grid:
    # x, y values from coordinate
    x = g[0]
    y = g[1]
    # make 200x200 array containing flow value, set all values 0 at initial
    flow = np.zeros((200, 200))
    # add +1 to flow value of rained grid
    flow[x][y] += 1
    # crop array having rained grid at the middle and surrounding grids
    # This allows water to flow diagonally
    surrounding = height_float[x-1:x+2, y-1:y+2]

    # if cropped array is 3x3, loop to find which of the surrounding grids
    # will get water from the grid which water is flowing
    while surrounding.shape == (3, 3):
        # make list of coordinates of all cropped grids
        surr_coor = [(i, j) for i in range(x-1, x+2) for j in range(y-1, y+2)]
        # make dict having coordinates of cropped, dry grids as keys
        # and their height as values
        surr_dict = {(i, j): height_list[i][j] for i in range(x-1,
                     x+2) for j in range(y-1, y+2) if flow[i][j] == 0}
        # make list of coordinates of cropped, dry grids having lowest height
        lowest = [k for k in surr_dict.keys()
                  if surr_dict[k] == min(list(surr_dict.values()))]
        # if all surrounding grids have been flowed through,
        # choose one of them randomly
        if len(lowest) == 0:
            next_grid = r.choice(surr_coor)
        # Otherwise, choose one of the lowest grids randomly
        else:
            next_grid = r.choice(lowest)
        # x, y values from coordinate of next grid which water flows through
        x = next_grid[0]
        y = next_grid[1]
        # add +1 to flow value of this grid
        flow[x][y] += 1
        # crop array having this grid at the middle and new surrounding grids
        surrounding = height_float[x-1:x+2, y-1:y+2]

    # When water moves from rained grid to edge of the area,
    # accumulate flow values (also called general relative water flow)
    cumulative_flow += flow

# Find index, kept in list, of grid having max general relative water flow
# The lake is believed that it contains this grid
max_water = np.where(cumulative_flow == cumulative_flow.max())
max_water_index = list(zip(max_water[0], max_water[1]))

# make 200x200 grid in 10km x 10km area
# y-axis is reversed in order to build (0, 0) at the bottom left of map
X, Y = np.meshgrid(np.linspace(0, 10, 200), np.linspace(10, 0, 200))
# name arrays used to build z-axis and/or colourbar
Zflow = cumulative_flow
Zheight = height_float
# Find coordinate of grid having max general relative water flow
xy = ((max_water_index[0][1])/20, (max_water_index[0][0])/20)
# make list of monthly rainfalls (mm) in Scotland Oct2019-Sep2020
# from https://www.statista.com/statistics/610092/monthly-rainfall-in-scotland/
rainfall = [148.5, 102.2, 189.8,
            209.5, 275.6, 123.3, 28.3, 76, 122.5, 135.4, 116.6, 121.8]
Month = ['Oct', 'Nov', 'Dec',
         'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep']

# create animation showing monthly change of relative water flow (general
# relative water flow multiplied by monthly rainfalls) from october 2019
# to september 2020

anime, ax1 = plt.subplots()  # create figure
plt.xlabel('x (km)')         # name x-axis
plt.ylabel('y (km)')         # name y-axis
# create contours and label heights in them
contour = ax1.contour(X, Y, Zheight, colors='#ff8526', alpha=0.75,
                      linewidths=0.6)
ax1.clabel(contour, fontsize=6, inline=True)
# note 'lake' at the grid having max general relative water flow to show
# where the lake is
ax1.annotate('lake', xy=xy)
# loop 12 times through list of rainfalls
for i in range(12):
    # make array of monthly, relative water flow
    monthly_flow = Zflow * rainfall[i]
    # create black-white colourmap of monthly, relative water flow with
    # log scale colourbar each month
    monthly_map = ax1.pcolor(X, Y, monthly_flow, shading='auto',  cmap='gray',
                             norm=LogNorm(vmin=(Zflow.min()*min(rainfall)),
                                          vmax=(Zflow.max()*max(rainfall))))
    cbar = anime.colorbar(monthly_map, ax=ax1)
    # create title of colorbar
    cbar.set_label('\nrelative water flow * monthly rainfall', rotation=90)
    # create title of map each month
    plt.title('Colourmap showing monthly, relative water flow\n\
in a 10km x 10km area in Scotland in %s %g' % (Month[i], ((i+9)//12)+2019))
    # display monthly map for 0.5 sec (may take longer due to low speed of run)
    plt.pause(0.5)
    # remove colourbar before displaying map for next month except for the last
    if i != 11:
        cbar.remove()
anime = plt.show()  # show animation

# tell users to wait for colourmap
print('Please wait for a colourmap for few seconds.')

# create figure
plt.figure()
map2D, ax3 = plt.subplots()
plt.xlabel('x (km)')  # name x-axis
plt.ylabel('y (km)')  # name y-axis
# create title of map
plt.title('Colourmap showing general relative water flow\n\
in a 10km x 10km area in Scotland')
# create black-white colourmap of general relative water flow with
# log scale colourbar
general_map = ax3.pcolor(X, Y, Zflow, shading='auto',
                         norm=LogNorm(vmin=(Zflow.min()), vmax=(Zflow.max())),
                         cmap='gray')
cbar2 = map2D.colorbar(general_map, ax=ax3)
# create title of colorbar
cbar2.set_label('\nrelative water flow', rotation=90)
# create contours and label heights in them
contour = ax3.contour(X, Y, Zheight, colors='#ff8526', alpha=0.75,
                      linewidths=0.6)
ax3.clabel(contour, fontsize=6, inline=True)
# note 'lake' where the lake is
ax3.annotate('lake', xy=xy)
# save map as cumulative_flow.png
plt.savefig('cumulative_flow.png', bbox_inches='tight')

# tell user map has been saved and good bye
print('The map has been saved.\nGood bye!')
