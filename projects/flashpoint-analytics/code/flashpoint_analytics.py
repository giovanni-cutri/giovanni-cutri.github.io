#!/usr/bin/env python
# coding: utf-8

# # Flashpoint Analytics
# 
# [Flashpoint](https://bluemaxima.org/flashpoint/) is a web-game preservation project, made in 2018 in an effort to save as many games as possible from the then upcoming Flash End-Of-Life, while also making them playable for everyone. Today, it hosts more than 170 000 games and thousands of active users all around the world.
# 
# This notebook contains a descriptive statistical analysis about the games available in Flashpoint, with an emphasis on categorical data, such as the technology that was used to make them or the publisher who used to host them in the past.
# 
# The Flashpoint database, which keeps all the data that will be used in the analysis, can be found [here](http://infinity.unstable.life/Flashpoint/Data/flashpoint.sqlite).

# ## Import modules

# In[1]:


import os
import urllib.request
import sqlite3
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import warnings


# These are the modules that we are going to use for our analysis. Notably:
# * *sqlite3* allows us to communicate with a SQLite database;
# * *pandas* offers very useful tools for working with data;
# * *seaborn* and *matplotlib* come with some handful functions to display and visualize data.

# ## Retrieve data

# In[2]:


os.mkdir("data")

# download data from the source

url = "http://infinity.unstable.life/Flashpoint/Data/flashpoint.sqlite"
filename = "data/flashpoint.sqlite"
urllib.request.urlretrieve(url, filename)

# connect to the database and store the "game" table in a dataframe

con = sqlite3.connect("data/flashpoint.sqlite")
df = pd.read_sql_query("SELECT * FROM game", con)
con.close()


# ## Explore data 

# Let's have a first look at our data.

# In[3]:


df.info()


# There is a total of 27 variables and almost all of them belong to the *object* data type. We are going to need only some of them, so let's keep only the relevant ones.

# In[4]:


vars_to_keep = ["id", "title", "developer", "publisher", "platform", "releaseDate", "language", "library", "tagsStr"]
df = df[vars_to_keep]
df.info()


# Among the remaining variables there are no missing values.

# To complete our preliminary analysis, let's print the first rows of our dataframe.

# In[5]:


df.head()


# ## Analyze data 

# ### Developers and Publishers

# It would be interesting to know which are the most prolific developers and publishers. Let's find out by creating a frequency table for each variable and looking at the first ten entries.

# In[6]:


top_developers = df["developer"].value_counts()[:10]
top_developers


# The first row is blank because some games (actually, most of them) do not have a developer value associated in the database. Let's filter out those entries.

# In[7]:


top_developers = df.loc[df.developer != '', "developer"].value_counts()[:10]
top_developers


# These are the most represented developers in the database. It is impressive to notice that almost all of them are known to be specialised in escape games, which we can suppose to be a very popular genre; we will dig into this later. Lastly, a special mention for Neopets, which managed to build a passionate community still active after over 20 years.

# In[8]:


top_publishers = df.loc[df.publisher != '', "publisher"].value_counts()[:10]
top_publishers


# Among the publishers, we can see some very renowned names, at least in the gaming community, like *Newgrounds*, *Armor Games* and *Kongregate*. There is also a considerable amount of games published by TV broadcasters, such as *Disney*, *Nickelodeon* and *Cartoon Network*, supposedly to promote their shows.

# Now let's look at a visualization of the same data, by making use of bar plots and pie charts.

# In[9]:


sns.barplot(x = top_developers.values, y = top_developers.index, orient = "h").set(title = "Top ten developers distribution");


# In[10]:


labels = top_developers.index
sizes = top_developers.values / top_developers.values.sum() * 100
plt.pie(sizes, textprops = {"color":"w"})
labels = [f"{l} - {s:0.1f}%" for l, s in zip(labels, sizes)]
plt.legend(labels = labels, bbox_to_anchor = (1.6,1), loc = "best")
plt.title("Top ten developers distribution")
plt.show()


# In[11]:


sns.barplot(x = top_publishers.values, y = top_publishers.index, orient = "h").set(title = "Top ten publishers distribution");


# In[12]:


labels = top_publishers.index
sizes = top_publishers.values / top_publishers.values.sum() * 100
plt.pie(sizes, textprops = {"color":"w"})
labels = [f"{l} - {s:0.1f}%" for l, s in zip(labels, sizes)]
plt.legend(labels = labels, bbox_to_anchor = (1.6,1), loc = "best")
plt.title("Top ten publishers distribution")
plt.show()


# ### Release Dates and Platforms

# Flash games started to appear towards the end of the twentieth century and became popular in the next decade. Let's observe the release dates we have got here, being aware that they are not specified for all games.

# In[13]:


df_dates = df.loc[(df.releaseDate != ""), ["title", "releaseDate", "platform", "library"]].sort_values(by=["releaseDate"])
df_dates


# There seems to be a problem with the data. Entries should follow the "YY-MM-DD" date format as per Flashpoint guidelines, but some games come in a different one. In addition, if the exact day or month of release is unknown, it is allowed to specify the year only. Let's clean up our data for consistency.

# In[14]:


warnings.filterwarnings("ignore", category = UserWarning)
df_dates["releaseDate"] = pd.to_datetime(df_dates["releaseDate"], errors = "coerce")
df_dates = df_dates.dropna().sort_values("releaseDate")
df_dates


# *Pandas* automatically assigned January 1 as month and day for those games whose only date information was the year.
# There is still one odd observation, the last one, which is most likely a typo.

# In[15]:


df_dates = df_dates[:-1]
df_dates[:20]


# Finally, we have got our correct release dates. We see that the oldest game in the list is *Blastar*, which was released in 1984. Actually, the game present in Flashpoint is a HTML5 version, which was developed and released much more recently. Moving on, starting from 1993 we recognize some old technologies, such as *Shochwave*, *VRML* and *Hyper-G*.
# 
# We can actually distinguish between proper games and animations by looking at the *library* column: the former are labeled with *arcade*, the latter with *theatre* values. Thus, the oldest animation featured is *Idle Johnny* from 1993, while the first "true" game (not counting *Blastar*) could be either *QP-Shot 1000* (which came out at some time in 1994), or *Virtual Banana Original* and *Virtual University of Auckland*, both from February 1st, 1994.

# In[16]:


df_dates = df_dates[1:]
df_dates[-20:]


# On the other side, here are the 20 most recent games. As expected, we find out that nowadays *HTML5* is the standard technology to make flash games, though some exceptions arise and there is even a *Flash* entry!

# For the sake of completeness, let's restrict our search to *Flash*-only games.

# In[17]:


df_dates.loc[(df_dates.platform == "Flash")][:20]


# The first *Flash* game is *Claus.com* from 1995. We notice that most of these are actually websites built in *Flash* and not exactly games or animations.

# To take an overall view, let's compare the various platforms by games count, considering the top five.

# In[18]:


top_platforms = df_dates["platform"].value_counts()[:5]
top_platforms


# In[19]:


colors = ["red", "orange", "green", "black", "blue"]
sns.barplot(x = top_platforms.values, y = top_platforms.index, orient = "h", palette = colors).set(title = "Top five platforms distribution");


# In[20]:


labels = top_platforms.index
sizes = top_platforms.values / top_platforms.values.sum() * 100
plt.pie(sizes, colors = colors, textprops = {"color":"w"})
labels = [f"{l} - {s:0.1f}%" for l, s in zip(labels, sizes)]
plt.legend(labels = labels, bbox_to_anchor = (1.5,1), loc = "best")
plt.title("Top five platforms distribution")
plt.show()


# *Flash* is clearly the winner, followed by a rising *HTML5* and its old companion *Shockwave*, with *Unity* and *Java* as outsiders.

# Web games were at their peak in the 2000s and many gamers are nostalgic about that decade, which could be considered a golden age. Thus, we expect to see that most of the games in our database have been released between 2000 and 2009. Let's check it out, while also comparing technologies against years.

# In[21]:


df_year_platform = df_dates.loc[(df_dates["platform"].isin(top_platforms.index)), :].copy()
years = df_year_platform["releaseDate"].astype(str).str[:4]
df_year_platform[df_year_platform.columns[1]] = years.values
df_year_platform.groupby(["releaseDate", "platform"]).size().unstack().plot(kind = 'bar', stacked = True, color = ["red", "orange", "blue", "green", "black"]);


# *Et voila*! As we were expecting, web games have steadily risen in popularity in the first decade of the third millennium, reached a peak in 2011 and today their number is slowly decreasing, apart from some fluctuations. This does not mean that fewer games are being made: it could simply be that there is less incentive to curate and preserve a recent game written in a technology which will probably stay on for a long time compared to an old game with a nostalgic value that runs the risk to disappear at any time.
# 
# *Flash* dominated the scene between 2000 and 2017 (it's impressive to see that it lasted so long), while *HTML5* started to be relevant around 2013. *Shockwave* was most popular between 1996 and 2000, but continued to be used until 2007. *Unity* had six years of relative notoriety (2010-2016) and lastly, Java, despite being one of the first technologies eligible for making web games, has never known much use and moved off the radar around 2010.

# ## Most common languages

# Let's move on to another topic: *Flashpoint* allows non-English content as well, and it can be interesting to know which countries have contributed the most to the world of web games aside from the anglophone ones.

# In[22]:


top_languages = df.loc[df["language"] != "", "language"].str.replace(",", ";").str.split("; ").explode().value_counts().drop("en")[:10]
top_languages


# Since a game can come in different languages, separated by a colon and a space ("; "), we had to count each occurrence individually.

# In[23]:


sns.barplot(x = top_languages.values, y = top_languages.index, orient = "h").set(title = "Top ten languages distribution");


# In[24]:


labels = top_languages.index
sizes = top_languages.values / top_languages.values.sum() * 100
plt.pie(sizes, textprops = {"color":"w"})
labels = [f"{l} - {s:0.1f}%" for l, s in zip(labels, sizes)]
plt.legend(labels = labels, bbox_to_anchor = (1.4,1), loc = "best")
plt.title("Top ten languages distribution")
plt.show()


# We can see a strong presence of Asian content, with Japanese, Korean and Chinese among the top ten languages. The rest of the list is completed by European countries, namely Portugal, Spain, France, Germany, Poland and Italy, as well as Russia.

# ## Most popular genres

# Let's now focus on game genres, featured on the *tagsStr* column, to discover the most common ones.

# In[25]:


top_genres = df.loc[df["tagsStr"] != "", "tagsStr"].str.replace(",", ";").str.split("; ").explode().value_counts()[:10]
top_genres


# In[26]:


sns.barplot(x = top_genres.values, y = top_genres.index, orient = "h").set(title = "Top ten genres distribution");


# In[27]:


labels = top_genres.index
sizes = top_genres.values / top_genres.values.sum() * 100
plt.pie(sizes, textprops = {"color":"w"})
labels = [f"{l} - {s:0.1f}%" for l, s in zip(labels, sizes)]
plt.legend(labels = labels, bbox_to_anchor = (1.6,1), loc = "best")
plt.title("Top ten genres distribution")
plt.show()


# The big three genres are *Arcade*, *Puzzle* and *Adventure* and honestly it's kind of odd to see *Action* at such a low position. Conversely, as we expected from our previous analysis on developers, *Escape the Room* is fairly popular, along with *Dress Up* and *Simulation* games.

# ## Most played games

# As a final insight, let's find out which are the most played games among the *Flashpoint* users: to do this, we are going to use some official statistics from the platform itself. Visit https://flashpoint-analytics.unstable.life/, scroll down to the corresponding section and download the data in .csv format.

# In[28]:


most_played = pd.read_csv("data/most_played.csv")
most_played.rename(columns = {"category": "id"}, inplace = True)
most_played


# The file contains the *id* for the most 40 played games, along with a play count. Let's use the identifiers to find the titles of these games and their other info.

# In[29]:


df_rank = df.merge(most_played, on = "id").sort_values("Play Count", ascending = False).reset_index()
df_rank


# In[30]:


fig, ax = plt.subplots(figsize=(10, 15))
sns.barplot(x = df_rank["Play Count"][:40], y = df_rank["title"][:40], orient = "h", ax = ax).set(title = "Top forty Flashpoint games by play count");


# There we go! *Poptropica* is the indisputable winner, with almost fifty thousand play counts. There is a massive presence of *Papa's Gameria* franchise, as well as all-time classics like *Strike Force Heroes*, *Super Mario 63* and *Age of War*. Finally, a special remark about *Ben 10: Battle Ready*, which was thought to be lost forever, before it was restored and made playable again on *Flashpoint*.

# ## Conclusion

# This was a thorough analysis of the *Flashpoint* catalogue, which hopefully gives some insights about the world of web-based games and their significant relevance in the history of the Internet.
# 
# The effort to preserve this kind of content has generated amazing results, saving an astounding quantity of material which would have disappeared otherwise. Despite the concrete risk of a digital dark age, we should insist on preserving the stuff that we care about and keep it alive, not only for historical reasons, but also for the nostalgic value we associate with it.
