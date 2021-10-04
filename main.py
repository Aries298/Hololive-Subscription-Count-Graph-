import json
import urllib.request
import time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import style
from data import key, arrholo, arrcolors, urlist

# Declaring variables and dictionaries
timestr = time.strftime("%d%m%Y")
timestr2 = time.strftime("%d.%m.%Y")
style.use("seaborn-bright")
xaxis = 0
yaxis = 0
i = 0
urls = dict()
datalist = dict()
arrscore = np.empty(len(arrholo))

# Function to cut unnecessary space
def trunc(string):
    return string.replace(" ", "")

# Iterating through the lists in data file
for x in range(len(arrholo)):
    urls[x] = trunc(arrholo[x]) + "_url"
    urls[trunc(arrholo[x]) + "_url"] = "https://www.googleapis.com/youtube/v3/channels?part=statistics&id=" + urlist[
        x] + "&key=" + key
    datalist[x] = trunc(arrholo[x]) + "_data"
    datalist[trunc(arrholo[x]) + "_data"] = urllib.request.urlopen(urls[trunc(arrholo[x] + "_url")]).read()
    arrscore[x] = int(json.loads(datalist[trunc(arrholo[x]) + "_data"])["items"][0]["statistics"]["subscriberCount"])
# Sorting the lists subscriptionwise
yaxis = np.sort(arrscore)[::-1]
arrscore = np.argsort(arrscore)
arrscore[::-1].argsort()
arrscore = arrscore[::-1]
sortedcolors = arrcolors[arrscore]
xaxis = arrholo[arrscore]

# Creating the chart
plt.rcParams.update({'font.size': 8})
plt.figure(figsize=(70, 10))
ax = plt.gca()
barlist = plt.bar(xaxis, yaxis, width=0.5)

plt.title(timestr2)
for i in range(len(barlist)):
    barlist[i].set_color(sortedcolors[i])
data = pd.DataFrame(xaxis, yaxis)

# print all exact values for confirmation
print(data)

# Make some labels to describe each bar
rects = ax.patches
labels = [int(yaxis[i]) for i in range(len(rects))]

for rect, label in zip(rects, labels):
    height = rect.get_height()
    ax.text(rect.get_x() + rect.get_width() / 2, height + 5, label,
            ha='center', va='bottom')

# Save the figure and show
plt.savefig("Chart from " + timestr)
plt.show()
